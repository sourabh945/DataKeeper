
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
 
import io

### local imports ######################################################

from modules.__helper__.mimetypes import mimetype

########################################################################

### request functions

class requests:

    @httperrors
    def ls(**kwargs) -> list[dict]:
        """ls is function that request the list in files using api and return the result"""
        request = (
            service.files()
            .list(**kwargs)
            .execute()
        )
        return request

    @httperrors
    def create(**kwargs) -> list[dict]:
        """create is function that request to create a folder/file in the drive using api """
        request = (
            service.files()
            .create(**kwargs)
            .execute()
        )
        return request

    @httperrors
    def get(**kwargs) -> list[dict]:
        """get is function that request to get file/folder info in the drive using api"""
        request = (
            service.files()
            .get(**kwargs)
            .execute()
        )
        return request 

    @httperrors
    def update(**kwargs) -> list[dict]:
        """update is function that request to update the meta-data in the drive using api"""
        request = (
            service.files()
            .update(**kwargs)
            .execute()
        )
        return request

    @httperrors
    def get_media(**kwargs) :
        """get_media is function that request the dow"""
        service.files().get_media()