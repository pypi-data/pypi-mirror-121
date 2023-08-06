import getpass
xKHUI=object
xKHUM=staticmethod
xKHUD=False
xKHUS=Exception
xKHUO=None
xKHUL=input
xKHUQ=list
import json
import logging
import sys
from localstack.config import CONFIG_FILE_PATH,load_config_file
from localstack.constants import API_ENDPOINT
from localstack.utils.common import load_file,safe_requests,save_file,to_str
LOG=logging.getLogger(__name__)
class AuthProvider(xKHUI):
 @xKHUM
 def name():
  raise
 def get_or_create_token(self,username,password,headers):
  pass
 def get_user_for_token(self,token):
  pass
 @xKHUM
 def providers():
  return{c.name():c for c in AuthProvider.__subclasses__()}
 @xKHUM
 def get(provider,raise_error=xKHUD):
  provider_class=AuthProvider.providers().get(provider)
  if not provider_class:
   msg='Unable to find auth provider class "%s"'%provider
   LOG.warning(msg)
   if raise_error:
    raise xKHUS(msg)
   return xKHUO
  return provider_class()
class AuthProviderInternal(AuthProvider):
 @xKHUM
 def name():
  return "internal"
 def get_or_create_token(self,username,password,headers):
  data={"username":username,"password":password}
  response=safe_requests.post("%s/user/signin"%API_ENDPOINT,json.dumps(data),headers=headers)
  if response.status_code>=400:
   return
  try:
   result=json.loads(to_str(response.content or "{}"))
   return result["token"]
  except xKHUS:
   pass
 def read_credentials(self,username):
  print("Please provide your login credentials below")
  if not username:
   sys.stdout.write("Username: ")
   sys.stdout.flush()
   username=xKHUL()
  password=getpass.getpass()
  return username,password,{}
 def get_user_for_token(self,token):
  raise xKHUS("Not implemented")
def login(provider,username=xKHUO):
 auth_provider=AuthProvider.get(provider)
 if not auth_provider:
  providers=xKHUQ(AuthProvider.providers().keys())
  raise xKHUS('Unknown provider "%s", should be one of %s'%(provider,providers))
 username,password,headers=auth_provider.read_credentials(username)
 print("Verifying credentials ... (this may take a few moments)")
 token=auth_provider.get_or_create_token(username,password,headers)
 if not token:
  raise xKHUS("Unable to verify login credentials - please try again")
 configs=load_config_file()
 configs["login"]={"provider":provider,"username":username,"token":token}
 save_file(CONFIG_FILE_PATH,json.dumps(configs))
def logout():
 configs=json_loads(load_file(CONFIG_FILE_PATH,default="{}"))
 configs["login"]={}
 save_file(CONFIG_FILE_PATH,json.dumps(configs))
def json_loads(s):
 return json.loads(to_str(s))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
