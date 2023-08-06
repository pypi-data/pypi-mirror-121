from localstack.utils.aws import aws_models
xbhlR=super
xbhlq=None
xbhlg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  xbhlR(LambdaLayer,self).__init__(arn)
  self.cwd=xbhlq
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.xbhlg.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,xbhlg,env=xbhlq):
  xbhlR(RDSDatabase,self).__init__(xbhlg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,xbhlg,env=xbhlq):
  xbhlR(RDSCluster,self).__init__(xbhlg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,xbhlg,env=xbhlq):
  xbhlR(AppSyncAPI,self).__init__(xbhlg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,xbhlg,env=xbhlq):
  xbhlR(AmplifyApp,self).__init__(xbhlg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,xbhlg,env=xbhlq):
  xbhlR(ElastiCacheCluster,self).__init__(xbhlg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,xbhlg,env=xbhlq):
  xbhlR(TransferServer,self).__init__(xbhlg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,xbhlg,env=xbhlq):
  xbhlR(CloudFrontDistribution,self).__init__(xbhlg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,xbhlg,env=xbhlq):
  xbhlR(CodeCommitRepository,self).__init__(xbhlg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
