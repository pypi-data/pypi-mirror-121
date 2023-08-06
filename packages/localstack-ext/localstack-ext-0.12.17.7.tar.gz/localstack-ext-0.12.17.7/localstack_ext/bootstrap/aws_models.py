from localstack.utils.aws import aws_models
mrCLj=super
mrCLa=None
mrCLw=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  mrCLj(LambdaLayer,self).__init__(arn)
  self.cwd=mrCLa
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.mrCLw.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,mrCLw,env=mrCLa):
  mrCLj(RDSDatabase,self).__init__(mrCLw,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,mrCLw,env=mrCLa):
  mrCLj(RDSCluster,self).__init__(mrCLw,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,mrCLw,env=mrCLa):
  mrCLj(AppSyncAPI,self).__init__(mrCLw,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,mrCLw,env=mrCLa):
  mrCLj(AmplifyApp,self).__init__(mrCLw,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,mrCLw,env=mrCLa):
  mrCLj(ElastiCacheCluster,self).__init__(mrCLw,env=env)
class TransferServer(BaseComponent):
 def __init__(self,mrCLw,env=mrCLa):
  mrCLj(TransferServer,self).__init__(mrCLw,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,mrCLw,env=mrCLa):
  mrCLj(CloudFrontDistribution,self).__init__(mrCLw,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,mrCLw,env=mrCLa):
  mrCLj(CodeCommitRepository,self).__init__(mrCLw,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
