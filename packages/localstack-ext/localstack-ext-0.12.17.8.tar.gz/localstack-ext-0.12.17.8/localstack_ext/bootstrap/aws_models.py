from localstack.utils.aws import aws_models
AWqoK=super
AWqoH=None
AWqoc=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  AWqoK(LambdaLayer,self).__init__(arn)
  self.cwd=AWqoH
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.AWqoc.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,AWqoc,env=AWqoH):
  AWqoK(RDSDatabase,self).__init__(AWqoc,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,AWqoc,env=AWqoH):
  AWqoK(RDSCluster,self).__init__(AWqoc,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,AWqoc,env=AWqoH):
  AWqoK(AppSyncAPI,self).__init__(AWqoc,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,AWqoc,env=AWqoH):
  AWqoK(AmplifyApp,self).__init__(AWqoc,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,AWqoc,env=AWqoH):
  AWqoK(ElastiCacheCluster,self).__init__(AWqoc,env=env)
class TransferServer(BaseComponent):
 def __init__(self,AWqoc,env=AWqoH):
  AWqoK(TransferServer,self).__init__(AWqoc,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,AWqoc,env=AWqoH):
  AWqoK(CloudFrontDistribution,self).__init__(AWqoc,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,AWqoc,env=AWqoH):
  AWqoK(CodeCommitRepository,self).__init__(AWqoc,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
