from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

### from local modules import ################################

from modules.request import requests
from modules.error import is_exists, error, is_possible

###########################################################

class remote:

    def ls() -> list[dict]:
        """
        Retrieves a list of files from Google Drive.

        Returns:
            list[dict]: A list of dictionaries, each representing a file's metadata.
                         Returns an empty list if there are no files or an error occurs.
        """
        return requests.ls(q='trashed=false', field='files(id,parent,drive_id,name,modtime,size,mimeType,properties)').get('files')

    def create_folder(name: str, parents: str) -> str:
        """
        Creates a new folder in Google Drive.

        Args:
            name (str): The name of the folder to create.
            parents (str): The ID of the parent folder in Google Drive.

        Returns:
            str: The ID of the newly created folder, or None if creation fails.
        """

        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parents]
        }

        return requests.create(body=metadata, field='id').get('id')

    @is_exists
    def upload_file(path: str, metadata: dict, resumable: bool = False) -> str:
        """
        Uploads a file to Google Drive.

        Args:
            path (str): The local path to the file to upload.
            metadata (dict): A dictionary containing the file's metadata (e.g., name, parents).
            resumable (bool, optional): Whether to enable resumable uploads. Defaults to False.

        Returns:
            str: The ID of the uploaded file on Google Drive, or None if the upload fails.
        """

        file = MediaFileUpload(path, resumable=resumable)

        return requests.create(body=metadata, media_body=file, field='id').get('id')

    @is_exists
    def create_and_upload(path: str, metadata: dict, resumable: bool = False) -> str:
        """
        Creates a new file in Google Drive and uploads content to it.

        This function first generates a new file ID from Google Drive and then uses it 
        to create and upload the file.

        Args:
            path (str): The local path to the file to upload.
            metadata (dict): A dictionary containing the file's metadata (e.g., name, parents).
            resumable (bool, optional): Whether to enable resumable uploads. Defaults to False.

        Returns:
            str: The ID of the created and uploaded file on Google Drive, or None if the process fails.
        """

        id = requests.generateId(field='id').get('id') or None

        if id:
            metadata['id'] = id

            file = MediaFileUpload(path, resumable=resumable)

            return requests.create(body=metadata, media_body=file, field='id').get('id')

    def update(id: str, metadata: str) -> bool:
        """
        Updates the metadata of a file or folder in Google Drive.

        Args:
            id (str): The ID of the file or folder to update.
            metadata (str): A dictionary containing the updated metadata.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            requests.update(fileId=id, body=metadata)
            return True
        except Exception as err:
            error(err)
            return False

    def get_metadata(id: str) -> dict:
        """
        Retrieves the metadata of a file or folder in Google Drive.

        Args:
            id (str): The ID of the file or folder.

        Returns:
            dict: A dictionary containing the metadata of the file or folder.
        """
        return requests.get(fileId=id, field='files(id,parent,drive_id,name,modtime,size,mimeType,properties)').get('files')

    @is_possible
    def download(id: str, path: str) -> bool:
        """
        Downloads a file from Google Drive.

        Args:
            id (str): The ID of the file on Google Drive.
            path (str): The local path where the file should be saved.

        Returns:
            bool: True if the download was successful, False otherwise.
        """

        request = requests.get_media(fileId=id)

        if request:
            try:
                with open(path, 'wb') as file:
                    downloader = MediaIoBaseDownload(file, request)
                    done = False
                    while not done:
                        _, done = downloader.next_chunk()
                return True
            except Exception as err:
                error(err)
                return False
        else:
            return False
