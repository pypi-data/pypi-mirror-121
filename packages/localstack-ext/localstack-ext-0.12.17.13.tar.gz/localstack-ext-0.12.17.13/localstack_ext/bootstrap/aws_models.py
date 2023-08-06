from localstack.utils.aws import aws_models
zhegf=super
zhegY=None
zhegj=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  zhegf(LambdaLayer,self).__init__(arn)
  self.cwd=zhegY
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.zhegj.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,zhegj,env=zhegY):
  zhegf(RDSDatabase,self).__init__(zhegj,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,zhegj,env=zhegY):
  zhegf(RDSCluster,self).__init__(zhegj,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,zhegj,env=zhegY):
  zhegf(AppSyncAPI,self).__init__(zhegj,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,zhegj,env=zhegY):
  zhegf(AmplifyApp,self).__init__(zhegj,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,zhegj,env=zhegY):
  zhegf(ElastiCacheCluster,self).__init__(zhegj,env=env)
class TransferServer(BaseComponent):
 def __init__(self,zhegj,env=zhegY):
  zhegf(TransferServer,self).__init__(zhegj,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,zhegj,env=zhegY):
  zhegf(CloudFrontDistribution,self).__init__(zhegj,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,zhegj,env=zhegY):
  zhegf(CodeCommitRepository,self).__init__(zhegj,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
