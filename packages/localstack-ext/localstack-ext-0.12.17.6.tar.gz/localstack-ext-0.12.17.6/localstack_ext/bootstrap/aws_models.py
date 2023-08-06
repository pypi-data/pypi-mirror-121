from localstack.utils.aws import aws_models
CxVvP=super
CxVvG=None
CxVvB=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  CxVvP(LambdaLayer,self).__init__(arn)
  self.cwd=CxVvG
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.CxVvB.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,CxVvB,env=CxVvG):
  CxVvP(RDSDatabase,self).__init__(CxVvB,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,CxVvB,env=CxVvG):
  CxVvP(RDSCluster,self).__init__(CxVvB,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,CxVvB,env=CxVvG):
  CxVvP(AppSyncAPI,self).__init__(CxVvB,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,CxVvB,env=CxVvG):
  CxVvP(AmplifyApp,self).__init__(CxVvB,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,CxVvB,env=CxVvG):
  CxVvP(ElastiCacheCluster,self).__init__(CxVvB,env=env)
class TransferServer(BaseComponent):
 def __init__(self,CxVvB,env=CxVvG):
  CxVvP(TransferServer,self).__init__(CxVvB,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,CxVvB,env=CxVvG):
  CxVvP(CloudFrontDistribution,self).__init__(CxVvB,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,CxVvB,env=CxVvG):
  CxVvP(CodeCommitRepository,self).__init__(CxVvB,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
