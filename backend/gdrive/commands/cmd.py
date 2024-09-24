from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
import os
import queue


### from local modules import ################################

from ..modules.request import requests
from ..modules.error import is_exists, error, is_possible

###########################################################

class remote:
    """
    Provides methods for interacting with a remote Google Drive storage.
    """
    def ls() -> list[dict]:
        """
        Retrieves a list of files from Google Drive.

        Returns:
            list[dict]: A list of dictionaries, each representing a file's metadata.
                         Returns an empty list if there are no files or an error occurs.
        """
        return (requests.ls(q='trashed=false',spaces='drive', fields='files(id,parents,drive_id,name,modifiedTime,size,mimeType,properties)')).get('files', [])

    def root_id() -> str:
        """
        Retrieves the ID of the root folder in Google Drive.

        Returns:
            str: The ID of the root folder.
        """
        return requests.get(fileId='root', fields='id').get('id')



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

        return requests.create(body=metadata, fields='id').get('id') or None

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

        return requests.create(body=metadata, media_body=file, fields='id').get('id')

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

        id = requests.generateId(fields='id').get('id') or None

        if id:
            metadata['id'] = id

            file = MediaFileUpload(path, resumable=resumable)

            return requests.create(body=metadata, media_body=file, fields='id').get('id')

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
        return requests.get(fileId=id, fields='files(id,parents,drive_id,name,modtime,size,mimeType,properties)').get('files')

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

    #############################################################################################33
    class functions:
        """
        Provides asynchronous functions for file operations.
        """
        def _create_folder(item:dict,q:queue.Queue):
            """
            Creates a folder asynchronously.

            Args:
                item (dict): A dictionary containing folder information.
                q (queue.Queue): A queue to put the result in.
            """
            print(f'[ Creating ] folder: {item["path"]}')

            res = remote.create_folder(os.path.basename(item['path']),item['parents'])


            if res:

                print(f'[ Done ] folder: {item["path"]}')

                q.put((item['path'],res))

            else:

                print(f'[ Fail ] folder: {item["path"]}')

                q.put((item['path'],res))


        def _upload_file(item:dict,q:queue.Queue):
            """
            Uploads a file asynchronously.

            Args:
                item (dict): A dictionary containing file information.
                q (queue.Queue): A queue to put the result in.
            """
            print(f'[ Uploading ] file: {item["path"]}')

            metadata = {
                'name': os.path.basename(item['path']),
                'parents': item['parents'],
                'properties': {
                    'version':item['version'],
                    'other_version':item['other_version']
                    },
                'description':f'version:{item['version']} | local_path:{item["path"]}',
                'modifiedTime':item['modtime']
            }

            resumable = True if item['size']/(1024*1024) > 5 else False
            
            res = remote.upload_file(item['path'],metadata,resumable)

            if res:

                print(f'[ Done ] file: {item["path"]}')

                q.put((item['path'],res))

            else:

                print(f'[ Fail ] file: {item["path"]}')

                q.put((item['path'],res))


        def _update_file(item:dict,q:queue.Queue):
            """
            Updates a file asynchronously.

            Args:
                item (dict): A dictionary containing file information.
                q (queue.Queue): A queue to put the result in.
            """
            print(f'[ Updating ] file: {item["path"]}')

            metadata = {
                'properties': {
                    'version':item['version'],
                    'other_version':item['other_version']
                    },
                'description':f'version:{item['version']} | local_path:{item["path"]}',
                'modifiedTime':item['modtime']
            }

            res = remote.update(item['id'],metadata)

            if res:

                print(f'[ Done ] file: {item["path"]}')

                q.put((item['path'],res))

            else:

                print(f'[ Fail ] file: {item["path"]}')

                q.put((item['path'],res))



        def _create_and_upload_file(item:dict,q:queue.Queue):
            """
            Creates and uploads a file asynchronously.

            Args:
                item (dict): A dictionary containing file information.
                q (queue.Queue): A queue to put the result in.
            """
            print(f'[ Creating and Uploading ] file: {item["path"]}')

            metadata = {
                'name': os.path.basename(item['path']),
                'parents': item['parents'],
                'properties': {
                    'version':item['version'],
                    'other_version':item['other_version']
                    },
                'description':f'version:{item['version']} | local_path:{item["path"]}',
                'modifiedTime':item['modtime']
            }

            resumable = True if item['size']/(1024*1024) > 5 else False
            
            res = remote.create_and_upload(item['path'],metadata,resumable)

            if res:

                print(f'[ Done ] file: {item["path"]}')

                q.put((item['path'],res))

            else:

                print(f'[ Fail ] file: {item["path"]}')

                q.put((item['path'],res))



        def _download_file(item:dict,q:queue.Queue):
            """
            Downloads a file asynchronously.

            Args:
                item (dict): A dictionary containing file information.
                q (queue.Queue): A queue to put the result in.
            """
            print(f'[ Downloading ] file: {item["path"]}')

            res = remote.download(item['id'],item['path'])

            if res:

                print(f'[ Done ] file: {item["path"]}')

                q.put((item['path'],res))

            else:

                print(f'[ Fail ] file: {item["path"]}')

                q.put((item['path'],res))
