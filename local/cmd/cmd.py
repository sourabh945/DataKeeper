

import os 
import datetime 
import json

### local imports #####################################

from paths import local_tree


class local :

    def ls_files(local_folder:str) -> list[dict]:
        """ls is function get the recursive list of the given folder """
        files_data = []
        for foldername, _, filenames in os.walk(local_folder):
            for filename in filenames:
                full_path = os.path.join(foldername, filename)
                relative_path = os.path.relpath(full_path, local_folder)
                
                # Get file size in bytes
                file_size = os.path.getsize(full_path)

                # Get last modified time in ISO 8601 format
                last_modified_timestamp = os.path.getmtime(full_path)
                last_modified = datetime.datetime.fromtimestamp(last_modified_timestamp)

                dt_utc = last_modified.astimezone(datetime.timezone.utc)

                last_modified_iso = dt_utc.isoformat()[:-9] + 'Z'

                files_data.append({
                    'name': filename,
                    'path': relative_path,
                    'size': file_size,
                    'modtime': last_modified_iso 
                })
        return files_data
    
    def ls_folders(local_folder:str) -> list[dict]:
        """ls is function get the recursive list of the given folder """
        folders_data = []
        for foldername, _, filenames in os.walk(local_folder):
            relative_path = os.path.relpath(foldername, local_folder)
            folders_data.append({
                'name': os.path.basename(foldername),
                'path': relative_path
            })
        return folders_data

    def ls(local_folder:str) -> list[dict]:
        """ls is function get the recursive list of the given folder """
        folders_data = local.ls_folders(local_folder)
        files_data = local.ls_files(local_folder)
        return folders_data + files_data

    def get_tree(local_folder:str) -> list[dict]:
        """get_tree is function get the recursive list of the given folder """
        return local.ls(local_folder)   

    def load_tree():
        if os.path.isfile(local_tree):
            with open(local_tree, 'r') as f:
                return json.load(f)
            
    
    def create_tree(local_data:list[dict],remote_data:list[dict]) -> list[dict]:

        local_ = set()

        tree = []

        for item in local_data:
            local_.add(item['name'],item['path'],item['modtime'],item['size'])

        tree_ = []


        for item in remote_data:

            if (item['name'],item['properties']['path'],item['modtime'],item['size']) in local_:
                local_.remove((item['name'],item['properties']['path'],item['modtime'],item['size']))

                temp_dict = {}
                temp_dict['name'] = item['name']
                temp_dict['path'] = item['properties']['path']
                temp_dict['modtime'] = item['modtime']
                temp_dict['size'] = item['size']
                temp_dict['id'] = item['id']
                temp_dict['version'] = item['properties']['version']
                temp_dict['parents'] = item['parents']
                temp_dict['drive_id'] = item['drive_id']
                
                tree_.append(temp_dict)

        tree.append({'in_remote':tree_})

        tree_ = []


        for item in local_:
            temp_dict = {}
            temp_dict['name'] = item[0]
            temp_dict['path'] = item[1]
            temp_dict['modtime'] = item[2]
            temp_dict['size'] = item[3]

            tree_.append(temp_dict)
        
        tree.append({'not_in_remote':tree_})

        return tree
    
    def save_tree(tree:list[dict]):
        with open(local_tree, 'w') as f:
            json.dump(tree, f)


    