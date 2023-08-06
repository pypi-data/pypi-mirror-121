from localstack.utils.aws import aws_models
ODPHU=super
ODPHc=None
ODPHR=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  ODPHU(LambdaLayer,self).__init__(arn)
  self.cwd=ODPHc
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.ODPHR.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,ODPHR,env=ODPHc):
  ODPHU(RDSDatabase,self).__init__(ODPHR,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,ODPHR,env=ODPHc):
  ODPHU(RDSCluster,self).__init__(ODPHR,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,ODPHR,env=ODPHc):
  ODPHU(AppSyncAPI,self).__init__(ODPHR,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,ODPHR,env=ODPHc):
  ODPHU(AmplifyApp,self).__init__(ODPHR,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,ODPHR,env=ODPHc):
  ODPHU(ElastiCacheCluster,self).__init__(ODPHR,env=env)
class TransferServer(BaseComponent):
 def __init__(self,ODPHR,env=ODPHc):
  ODPHU(TransferServer,self).__init__(ODPHR,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,ODPHR,env=ODPHc):
  ODPHU(CloudFrontDistribution,self).__init__(ODPHR,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,ODPHR,env=ODPHc):
  ODPHU(CodeCommitRepository,self).__init__(ODPHR,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
