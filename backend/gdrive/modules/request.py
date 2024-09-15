
"""----------------------------------------------------------------------------------------------------------------------------"""

################### service builder ###################################

from google.auth.credentials import Credentials
from googleapiclient import discovery
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

    ######### local imports #############################

from modules.tokenizer import tokenizer
from modules.error import error,httperrors

    ####################################################


def service_builder(token:Credentials) -> discovery.Resource:
    """ this function build the service to perform the request to the api """
    try:
        service = build('drive','v3',credentials=token)
        return service
    except HttpError as err:
        message = f'[ {err.status_code} ] [ {err.reason} ] {err.content} \n unable to build the service please check your internet connection.'
        error(message,True,1)

service = service_builder(tokenizer())

########################################################################

"""------------------------------------------------------------------------------------------------------------------------------"""

import os 
import io

### google api imports #################################################

from googleapiclient.http import MediaDownloadProgress,MediaFileUpload

### local imports ######################################################

from modules.__helper__.mimetypes import mimetype

########################################################################


def ls(**kwargs) -> list[dict]:
    request = (
        service.files()
        .list(**kwargs)
        .execute()
    )
    return request