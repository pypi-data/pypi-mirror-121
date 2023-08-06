from localstack.utils.aws import aws_models
qIpiQ=super
qIpiD=None
qIpiW=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  qIpiQ(LambdaLayer,self).__init__(arn)
  self.cwd=qIpiD
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.qIpiW.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,qIpiW,env=qIpiD):
  qIpiQ(RDSDatabase,self).__init__(qIpiW,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,qIpiW,env=qIpiD):
  qIpiQ(RDSCluster,self).__init__(qIpiW,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,qIpiW,env=qIpiD):
  qIpiQ(AppSyncAPI,self).__init__(qIpiW,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,qIpiW,env=qIpiD):
  qIpiQ(AmplifyApp,self).__init__(qIpiW,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,qIpiW,env=qIpiD):
  qIpiQ(ElastiCacheCluster,self).__init__(qIpiW,env=env)
class TransferServer(BaseComponent):
 def __init__(self,qIpiW,env=qIpiD):
  qIpiQ(TransferServer,self).__init__(qIpiW,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,qIpiW,env=qIpiD):
  qIpiQ(CloudFrontDistribution,self).__init__(qIpiW,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,qIpiW,env=qIpiD):
  qIpiQ(CodeCommitRepository,self).__init__(qIpiW,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
