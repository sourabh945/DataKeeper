
import os 

### google api imports ######################################

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


### local imports ##########################################

from paths import token_path
from _secrets_.gdrive_credentials import gdrive_api_key 
from __scopes__ import SCOPE

#########################################################

def make_folder():

    if not os.path.isdir(os.path.sep(token_path)):
        os.mkdir(os.path.sep(token_path))

make_folder()

def tokenizer() -> Credentials:

    token = None

    if os.path.exists(token_path):
        token = Credentials.from_authorized_user_file(token_path)
    if not token or not token.valid:
        if token and token.expired and token.refresh_token:
            token.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(gdrive_api_key,SCOPE)
            token = flow.run_local_server(port=0)
        with open(token_path,'w') as file:
            file.write(token.to_json())

    return token