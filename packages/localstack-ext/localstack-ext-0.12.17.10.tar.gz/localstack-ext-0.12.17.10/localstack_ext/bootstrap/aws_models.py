from localstack.utils.aws import aws_models
ptOFr=super
ptOFG=None
ptOFg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  ptOFr(LambdaLayer,self).__init__(arn)
  self.cwd=ptOFG
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.ptOFg.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,ptOFg,env=ptOFG):
  ptOFr(RDSDatabase,self).__init__(ptOFg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,ptOFg,env=ptOFG):
  ptOFr(RDSCluster,self).__init__(ptOFg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,ptOFg,env=ptOFG):
  ptOFr(AppSyncAPI,self).__init__(ptOFg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,ptOFg,env=ptOFG):
  ptOFr(AmplifyApp,self).__init__(ptOFg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,ptOFg,env=ptOFG):
  ptOFr(ElastiCacheCluster,self).__init__(ptOFg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,ptOFg,env=ptOFG):
  ptOFr(TransferServer,self).__init__(ptOFg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,ptOFg,env=ptOFG):
  ptOFr(CloudFrontDistribution,self).__init__(ptOFg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,ptOFg,env=ptOFG):
  ptOFr(CodeCommitRepository,self).__init__(ptOFg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
