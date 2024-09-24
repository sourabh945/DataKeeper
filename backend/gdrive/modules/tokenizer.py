
import os 
import json

### google api imports ######################################

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials , _GOOGLE_OAUTH2_TOKEN_ENDPOINT
from google_auth_oauthlib.flow import InstalledAppFlow


### local imports ##########################################

from paths import token_path
from .._secrets_ import gdrive_api_key 
from ..__scopes__ import SCOPE
from .error import error

########################################################


#########################################################

def make_folder():

    if not os.path.isdir(os.path.dirname(token_path)):
        os.mkdir(os.path.dirname(token_path))

make_folder()

##########################################################

def load_token() -> Credentials:

    with open(token_path,'r') as file:
        half_token = json.load(file)

    token = {}

    try:

        token['token'] = half_token['token']
        token['refresh_token'] = half_token['refresh_token']
        token['token_uri'] = _GOOGLE_OAUTH2_TOKEN_ENDPOINT

        token['client_id'] = gdrive_api_key['client_id']
        token['client_secret'] = gdrive_api_key['client_secret']

        token['quota_project_id'] = gdrive_api_key.get('quota_project_id')
        token['expiry'] = half_token['expiry']
        token['rapt_token'] = half_token.get('rapt_token')
        token['trust_boundary'] = half_token.get('trust_boundary')
        token['universe_domain'] = half_token.get('universe_domain')
        token['account'] = half_token.get('account')

        return Credentials.from_authorized_user_info(token,SCOPE)

    except Exception as err:

        error(err,exit_=True)

##########################################################

def tokenizer() -> Credentials:
    
    try:

        token = None

        if os.path.exists(token_path):
    
            token = load_token()

        else:
            print("\nPlease login the to with using gmail account where you wanted to backup the folder. And don't worry about thing all the access tokens are store locally no one can use it.")

            
        if not token or not token.valid:
            if token and token.expired and token.refresh_token:
                token.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(gdrive_api_key,scopes=SCOPE)
                token = flow.run_local_server(port=0)

            written_token = json.loads(token.to_json())

            written_token['client_id'] = "***encrpyted***"
            written_token['client_secret'] = "***encrpyted***"

            with open(token_path,'w') as file:
                json.dump(written_token,file)

        return token
    
    except Exception as err:

        print('\nUnable to connect the drive. Please check your internet or dns or vpn settings.\nThe error is : \n')

        error(err,exit_=True)

        