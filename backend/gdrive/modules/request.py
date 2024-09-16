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
    """
    Builds the Google Drive API service object.

    Args:
        token (Credentials): Google API credentials object.

    Returns:
        discovery.Resource: A Google Drive API service object.
    """
    try:
        service = build('drive','v3',credentials=token)
        return service
    except HttpError as err:
        message = f'[ {err.status_code} ] [ {err.reason} ] {err.content} \n unable to build the service please check your internet connection.'
        error(message,True,1)

service = service_builder(tokenizer())

########################################################################

"""------------------------------------------------------------------------------------------------------------------------------"""

from tenacity import retry, stop_after_attempt, wait_exponential


### local imports ######################################################

from modules.__helper__.mimetypes import mimetype

########################################################################

### request functions

class requests:
    """
    A class to handle requests to the Google Drive API.
    """

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    @httperrors
    def ls(**kwargs) -> list[dict]:
        """
        Lists files in Google Drive.

        Args:
            **kwargs: Keyword arguments to pass to the API request.

        Returns:
            list[dict]: A list of dictionaries, each representing a file.
        """
        request = (
            service.files()
            .list(**kwargs)
            .execute()
        )
        return request

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    @httperrors
    def create(**kwargs) -> list[dict]:
        """
        Creates a new file or folder in Google Drive.

        Args:
            **kwargs: Keyword arguments to pass to the API request.

        Returns:
            list[dict]: A list containing the created file or folder.
        """
        request = (
            service.files()
            .create(**kwargs)
            .execute()
        )
        return request
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    @httperrors
    def generateId(**kwargs) -> list[dict]:
        """
        Generates a new file ID in Google Drive.

        Args:
            **kwargs: Keyword arguments to pass to the API request.

        Returns:
            list[dict]: A list containing the generated file ID.
        """
        request = (
            service.files()
            .generateId(**kwargs)
            .execute()
        )
        return request

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    @httperrors
    def get(**kwargs) -> list[dict]:
        """
        Gets the metadata of a file or folder in Google Drive.

        Args:
            **kwargs: Keyword arguments to pass to the API request.

        Returns:
            list[dict]: A list containing the metadata of the file or folder.
        """
        request = (
            service.files()
            .get(**kwargs)
            .execute()
        )
        return request 

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    @httperrors
    def update(**kwargs) -> list[dict]:
        """
        Updates the metadata of a file or folder in Google Drive.

        Args:
            **kwargs: Keyword arguments to pass to the API request.

        Returns:
            list[dict]: A list containing the updated metadata of the file or folder.
        """
        request = (
            service.files()
            .update(**kwargs)
            .execute()
        )
        return request

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    @httperrors
    def get_media(**kwargs) :
        """
        Downloads the content of a file from Google Drive.

        Args:
            **kwargs: Keyword arguments to pass to the API request.

        Returns:
            The downloaded file content.
        """
        request = (
            service.files()
            .get_media(**kwargs)
            .execute()
        )
        return request
