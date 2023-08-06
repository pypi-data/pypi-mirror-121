from localstack.services.cloudformation.service_models import GenericBaseModel
zkhpu=None
zkhpN=classmethod
zkhpd=staticmethod
from localstack.utils.aws import aws_stack
class ServiceDiscoveryNamespace(GenericBaseModel):
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("servicediscovery")
  ns_name=self.resolve_refs_recursively(stack_name,self.props["Name"],resources)
  namespaces=client.list_namespaces()["Namespaces"]
  namespace=[ns for ns in namespaces if ns["Type"]==self._type()and ns["Name"]==ns_name]
  return(namespace or[zkhpu])[0]
 def get_physical_resource_id(self,attribute,**kwargs):
  return self.props.get("Id")
 @zkhpN
 def get_deploy_templates(cls):
  def delete_params(resource_props,resources,resource_id,**kwargs):
   resource=cls(resources[resource_id])
   return{"Id":resource.props.get("Id")}
  create_func=cls._create_function()
  return{"create":{"function":create_func},"delete":{"function":"delete_namespace","parameters":delete_params}}
 def _type(self):
  raise
class ServiceDiscoveryService(ServiceDiscoveryNamespace):
 @zkhpd
 def cloudformation_type():
  return "AWS::ServiceDiscovery::Service"
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("servicediscovery")
  service_name=self.resolve_refs_recursively(stack_name,self.props["Name"],resources)
  services=client.list_services()["Services"]
  service=[s for s in services if s["Name"]==service_name]
  return(service or[zkhpu])[0]
 def get_physical_resource_id(self,attribute,**kwargs):
  if attribute=="Arn":
   return self.props.get("Arn")
  return self.props.get("Id")
 @zkhpN
 def get_deploy_templates(cls):
  def delete_params(resource_props,resources,resource_id,**kwargs):
   resource=cls(resources[resource_id])
   return{"Id":resource.props.get("Id")}
  return{"create":{"function":"create_service"},"delete":{"function":"delete_service","parameters":delete_params}}
class ServiceDiscoveryHttpNamespace(ServiceDiscoveryNamespace):
 @zkhpd
 def cloudformation_type():
  return "AWS::ServiceDiscovery::HttpNamespace"
 @zkhpN
 def _type(cls):
  return "HTTP"
 @zkhpN
 def _create_function(cls):
  return "create_http_namespace"
class ServiceDiscoveryPublicDnsNamespace(ServiceDiscoveryNamespace):
 @zkhpd
 def cloudformation_type():
  return "AWS::ServiceDiscovery::PublicDnsNamespace"
 @zkhpN
 def _type(cls):
  return "DNS_PUBLIC"
 @zkhpN
 def _create_function(cls):
  return "create_public_dns_namespace"
class ServiceDiscoveryPrivateDnsNamespace(ServiceDiscoveryNamespace):
 @zkhpd
 def cloudformation_type():
  return "AWS::ServiceDiscovery::PrivateDnsNamespace"
 @zkhpN
 def _type(cls):
  return "DNS_PRIVATE"
 @zkhpN
 def _create_function(cls):
  return "create_private_dns_namespace"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
