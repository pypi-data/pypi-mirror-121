import boto3
import functools
import os
import json
import mlflow
from urllib.parse import urlparse

INPUT_SPEC_CONFIG = os.getcwd() + "/infin-input-spec.conf"
declared_input_sources = []
class InfinBotoClient():
    def __init__(self, defaultClient, infinProxyClient, spec, bucket, prefix):
        # self.__class__ = type(baseObject.__class__.__name__,
        #                       (self.__class__, baseObject.__class__),
        #                       {})
        # self.__dict__ = baseObject.__dict__
        self.defaultClient = defaultClient
        self.infinProxyClient = infinProxyClient
        self.input_spec = spec
        self.bucket = bucket
        self.prefix = prefix

    def list_objects(self, *args, **kwargs):
        if self.input_spec['type'] == 'mlflow-run-artifacts':
            request_bucket = kwargs['Bucket']
            request_prefix = kwargs.get('Prefix')
            if is_declared_source(request_bucket, request_prefix):
                kwargs['Bucket'] = self.bucket
                if request_prefix:
                    kwargs['Prefix'] = self.prefix + "/" + request_prefix.lstrip('/')
                else:
                    kwargs['Prefix'] = self.prefix
                return self.defaultClient.list_objects(*args, **kwargs)
        elif self.input_spec['type'] == 'infinsnap' or self.input_spec['type'] == 'infinslice':
            return self.infinProxyClient.list_objects(*args, **kwargs)
        else:
            return self.defaultClient.list_objects(*args, **kwargs)

    def download_file(self, *args, **kwargs):
        if self.input_spec['type'] == 'mlflow-run-artifacts':
            request_bucket = args[0]
            request_file = args[1]
            if is_declared_source(request_bucket, request_file):
                arglist = list(args)
                arglist[0] = self.bucket
                if request_file:
                    arglist[1] = self.prefix + "/" + request_file.lstrip('/')
                else:
                    arglist[1] = self.prefix
                args = tuple(arglist)
                return self.defaultClient.download_file(*args, **kwargs)
        elif self.input_spec['type'] == 'infinsnap' or self.input_spec['type'] == 'infinslice':
            return self.infinProxyClient.download_file(*args, **kwargs)
        else:
            return self.defaultClient.download_file(*args, **kwargs)

    def __getattr__(self, attr):
        if attr == 'list_objects':
            return self.list_objects
        elif attr == 'download_file':
            return self.download_file
        else:
            return getattr(self.defaultClient, attr)

##Decorators are specific to functions

##Decorator for boto3.Session.client
def decorate_boto3_client(client_func):
    orig_func = client_func
    @functools.wraps(client_func)
    def wrapper(*args, **kwargs):
        defaultClient = orig_func(*args, **kwargs)
        if args[1] == 's3' and os.path.exists(INPUT_SPEC_CONFIG):
            spec, ep, bucket, prefix = get_endpoint_url(INPUT_SPEC_CONFIG)
            print(ep, bucket, prefix)
            if ep:
                kwargs['endpoint_url'] = ep
                #Create a new session
                arglist = list(args)
                arglist[0] = boto3.Session(profile_name='infinstor')
                args = tuple(arglist)
                infinProxyClient = orig_func(*args, **kwargs)
                return InfinBotoClient(defaultClient, infinProxyClient, spec, bucket, prefix)
            elif bucket:
                return InfinBotoClient(defaultClient, None, spec, bucket, prefix)
        return defaultClient
    return wrapper

def get_endpoint_url(config):
    with open(config) as fp:
        specs = json.load(fp)
        print("Loading specs#")
        print(specs)
    if specs['type'] == 'infinsnap' or specs['type'] == 'infinslice':
        time_spec = specs['time_spec']
        bucket = specs['bucketname']
        prefix = specs['prefix']
        service = specs['service']
        endpointurl = "https://{0}.s3proxy.{1}:443/".format(time_spec, service)
        if is_declared_source(bucket, prefix):
            return specs, endpointurl, bucket, prefix
        else:
            return specs, None, None, None
    elif specs['type'] == 'mlflow-run-artifacts':
        artifact_bucket, artifact_prefix = get_infin_output_location(run_id=specs['run_id'])
        if 'prefix' in specs:
            prefix = specs['prefix']
        else:
            prefix = artifact_prefix
        return specs, None, artifact_bucket, prefix
    return specs, None, None, None

def is_declared_source(bucket, prefix):
    for entry in declared_input_sources:
        if entry['bucket'] == bucket:
            return True
    return False

def declare_s3_source(bucket, prefix):
    src = {'bucket': bucket, 'prefix': prefix}
    declared_input_sources.append(src)

def get_infin_output_location(run_id=None, default_bucket=None, default_prefix="/"):
    if not run_id:
        active_run = mlflow.active_run()
        if active_run:
            run_id = mlflow.active_run().info.run_id
    if run_id:
        client = mlflow.tracking.MlflowClient()
        run = client.get_run(run_id)
        artifact_uri = run.info.artifact_uri
        parse_result = urlparse(artifact_uri)
        if (parse_result.scheme != 's3'):
            raise ValueError('Error. Do not know how to deal with artifacts in scheme ' \
                             + parse_result.scheme)
        bucketname = parse_result.netloc
        prefix = parse_result.path.lstrip('/')
        return bucketname, prefix
    else:
        return default_bucket, default_prefix

if os.path.exists(INPUT_SPEC_CONFIG):
    boto3.Session.client = decorate_boto3_client(boto3.Session.client)

###Intercepting Logic####
"""
1. User declares an input bucket
2. If input spec is infinsnap or infinslice
    If bucket in inputspec is same as declared input bucket
        change the endpoint url
        don't intercept any other calls --> THIS WILL CHANGE FOR PARTITIONING
    else
        don't change anything
3. If the input spec is mlflow artifact
    Don't change the endpoint url, but intercept the read/list
    if bucket in the call is same as declared input bucket
        change the bucket to the mlflow artifact uri bucket
    else
        don't do anything
"""