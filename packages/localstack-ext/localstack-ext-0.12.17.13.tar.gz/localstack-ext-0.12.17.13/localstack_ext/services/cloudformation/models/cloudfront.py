from localstack.services.cloudformation.service_models import REF_ID_ATTRS,GenericBaseModel
SmBio=staticmethod
SmBir=None
SmBiI=super
SmBiT=classmethod
SmBiX=isinstance
SmBiW=list
SmBib=set
SmBif=False
SmBiQ=str
SmBiH=dict
SmBih=len
from localstack.utils.aws import aws_stack
from localstack.utils.common import select_attributes,short_uid,to_bytes
from localstack_ext.utils.aws import aws_utils
class CloudFrontOriginAccessIdentity(GenericBaseModel):
 @SmBio
 def cloudformation_type():
  return "AWS::CloudFront::CloudFrontOriginAccessIdentity"
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("cloudfront")
  result=client.list_cloud_front_origin_access_identities()
  result=result.get("CloudFrontOriginAccessIdentityList",{}).get("Items",[])
  config=self.props.get("CloudFrontOriginAccessIdentityConfig",{})
  result=[r for r in result if r["Comment"]==config.get("Comment")]
  return result and result[0]or SmBir
 @SmBio
 def get_deploy_templates():
  def _params(params,**kwargs):
   config=params.get("CloudFrontOriginAccessIdentityConfig")
   config["CallerReference"]=short_uid()
   return params
  return{"create":{"function":"create_cloud_front_origin_access_identity","parameters":_params}}
class CloudFrontFunction(GenericBaseModel):
 @SmBio
 def cloudformation_type():
  return "AWS::CloudFront::Function"
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("cloudfront")
  result=client.list_functions()
  result=result.get("FunctionList",{}).get("Items",[])
  props=self.props
  result=[r for r in result if r["Name"]==props.get("Name")]
  return result and result[0]or SmBir
 def get_physical_resource_id(self,attribute,**kwargs):
  return self.props.get("Name")
 def get_cfn_attribute(self,attribute_name):
  if attribute_name=="FunctionARN":
   return aws_utils.get_cloudfront_function_arn(self.props.get("Name"))
  return SmBiI(CloudFrontFunction,self).get_cfn_attribute(attribute_name)
 @SmBiT
 def get_deploy_templates(cls):
  def _params(params,**kwargs):
   result=select_attributes(params,["Name","FunctionCode","FunctionConfig"])
   if result.get("FunctionCode"):
    result["FunctionCode"]=to_bytes(result["FunctionCode"])
   return result
  def _delete_function(resource_id,resources,resource_type,func,stack_name,*args):
   resource=cls(resources[resource_id])
   client=aws_stack.connect_to_service("cloudfront")
   name=resource.props.get("Name")
   etag=client.describe_function(Name=name).get("ETag")
   return client.delete_function(Name=name,IfMatch=etag)
  return{"create":{"function":"create_function","parameters":_params},"delete":{"function":_delete_function}}
class CloudFrontOriginRequestPolicy(GenericBaseModel):
 @SmBio
 def cloudformation_type():
  return "AWS::CloudFront::OriginRequestPolicy"
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("cloudfront")
  result=client.list_origin_request_policies()
  result=result.get("OriginRequestPolicyList",{}).get("Items",[])
  result=[r.get("OriginRequestPolicy",{})for r in result]
  result=[{"Id":r["Id"],**r.get("OriginRequestPolicyConfig",{})}for r in result]
  policy_name=self.props.get("OriginRequestPolicyConfig",{}).get("Name")
  policy_name=self.resolve_refs_recursively(stack_name,policy_name,resources)
  result=[r for r in result if r.get("Name")==policy_name]
  return result and result[0]or SmBir
 def get_physical_resource_id(self,attribute,**kwargs):
  return self.props.get("Id")
 @SmBiT
 def get_deploy_templates(cls):
  def _delete_policy(resource_id,resources,resource_type,func,stack_name,*args):
   client=aws_stack.connect_to_service("cloudfront")
   resource=cls(resources[resource_id])
   props=resource.props
   policy_id=props.get("OriginRequestPolicy").get("Id")
   etag=client.get_origin_request_policy(Id=policy_id).get("ETag")
   return client.delete_origin_request_policy(Id=policy_id,IfMatch=etag)
  return{"create":{"function":"create_origin_request_policy"},"delete":{"function":_delete_policy}}
class CloudFrontDistribution(GenericBaseModel):
 @SmBio
 def cloudformation_type():
  return "AWS::CloudFront::Distribution"
 def get_physical_resource_id(self,attribute,**kwargs):
  distr_id=self.props.get("Id")
  if attribute in REF_ID_ATTRS:
   return distr_id
  return aws_utils.get_cloudfront_distribution_arn(distr_id)
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("cloudfront")
  distrs=client.list_distributions()["DistributionList"].get("Items",[])
  props=self.props["DistributionConfig"]
  origins=props.get("Origins",[])
  origins=origins if SmBiX(origins,SmBiW)else origins.get("Items")
  origins_to_create=SmBib([orig["DomainName"]for orig in origins])
  aliases=props.get("Aliases",[])
  aliases=aliases if SmBiX(aliases,SmBiW)else aliases.get("Items")
  aliases_to_create=SmBib(aliases)
  for distr in distrs:
   origins=SmBib([orig.get("DomainName")for orig in distr.get("Origins",{})["Items"]])
   aliases=SmBib(distr.get("Aliases",{}).get("Items",[]))
   if origins_to_create==origins and aliases_to_create==aliases:
    return distr
 @SmBio
 def get_deploy_templates():
  def lambda_get_distribution_config(params,**kwargs):
   config=params["DistributionConfig"]
   config["CallerReference"]=config.get("CallerReference")or short_uid()
   config["Comment"]=config.get("Comment")or ""
   config["IsIPV6Enabled"]=config.pop("IPV6Enabled",SmBif)
   config["Enabled"]=SmBiQ(config.get("Enabled")).lower()=="true"
   cert=config["ViewerCertificate"]=config.get("ViewerCertificate",{})
   custom_errors=config.get("CustomErrorResponses",[])
   custom_errors=(custom_errors.get("Items",[])if SmBiX(custom_errors,SmBiH)else custom_errors)
   for item in custom_errors:
    item["ResponseCode"]=SmBiQ(item.get("ResponseCode"))
   cache=config["DefaultCacheBehavior"]
   cache["TrustedSigners"]=cache.get("TrustedSigners")or{"Quantity":0,"Enabled":SmBif}
   cache["MinTTL"]=cache.get("MinTTL")or 600
   forwarded=cache["ForwardedValues"]=cache.get("ForwardedValues",{})
   forwarded["QueryString"]=SmBiQ(forwarded.get("QueryString")).lower()=="true"
   if "AcmCertificateArn" in cert:
    cert["ACMCertificateArn"]=cert.pop("AcmCertificateArn")
   if "SslSupportMethod" in cert:
    cert["SSLSupportMethod"]=cert.pop("SslSupportMethod")
   if "IamCertificateId" in cert:
    cert["IAMCertificateId"]=cert.pop("IamCertificateId")
   params["Tags"]={"Items":params.get("Tags")or[]}
   def convert_list(key,parent=SmBir):
    parent=config if parent is SmBir else parent
    items=parent.get(key)or[]
    if SmBiX(items,SmBiH)and "Items" in items and "Quantity" in items:
     return
    parent[key]={"Quantity":SmBih(items),"Items":items}
   cache_behavs=config.get("CacheBehaviors",[])
   cache_behavs=(cache_behavs.get("Items",[])if SmBiX(cache_behavs,SmBiH)else cache_behavs)
   for cb in cache_behavs:
    convert_list("AllowedMethods",cb)
    cb["AllowedMethods"]["CachedMethods"]=cb.pop("CachedMethods",[])
    convert_list("CachedMethods",cb["AllowedMethods"])
   for origin in config["Origins"]:
    custom_origin_config=origin.get("CustomOriginConfig")
    if not custom_origin_config:
     continue
    custom_origin_config["OriginSslProtocols"]=custom_origin_config.pop("OriginSSLProtocols",[])
    custom_origin_config["HTTPPort"]=custom_origin_config.get("HTTPPort",80)
    custom_origin_config["HTTPSPort"]=custom_origin_config.get("HTTPSPort",443)
    convert_list("OriginSslProtocols",custom_origin_config)
   convert_list("Aliases")
   convert_list("Origins")
   convert_list("OriginGroups")
   convert_list("CustomErrorResponses")
   convert_list("CacheBehaviors")
   convert_list("AllowedMethods",cache)
   cache_behav=config.get("DefaultCacheBehavior",{})
   cache_behav["AllowedMethods"]=cache_behav.get("AllowedMethods")
   cache_behav["AllowedMethods"]["CachedMethods"]=config.get("DefaultCacheBehavior",{}).pop("CachedMethods",[])
   convert_list("CachedMethods",cache_behav["AllowedMethods"])
   if cache_behav.get("ForwardedValues")and not cache_behav["ForwardedValues"].get("Cookies"):
    cache_behav["ForwardedValues"]["Cookies"]={"Forward":"All"}
   restrs=config.get("Restrictions",{})
   if restrs.get("GeoRestriction")and "Quantity" not in restrs["GeoRestriction"]:
    restrs["GeoRestriction"]["Quantity"]=0
    restrs["GeoRestriction"]["Items"]=[]
   return params
  return{"create":{"function":"create_distribution_with_tags","parameters":{"DistributionConfigWithTags":lambda_get_distribution_config}}}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
