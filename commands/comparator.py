
import os 
from datetime import datetime as dt

def compare(backup_folder_path:str,local_:list[dict],remote_:list[dict]) -> list[dict]:
    """
    Compares the files and folders in a given folder.
    
    Args:
        backup_folder_path (str): The folder to compare.
        local_ (list[dict]): The list of local files and folders.
        remote_ (list[dict]): The list of remote files and folders.
    
    Returns:

        new folders, new files, deleted files, deleted folders, and modified files

        list[dict]: A list of dictionaries containing the files and folders.
    """


    local_folders , local_files = local_
    remote_folders , remote_files = remote_


    def _compare_folder(folder:str):
        """
        Compares the files and folders in a given folder.
        
        Args:
            folder (str): The folder to compare.
        
        Returns:

            tuple: A tuple containing the new folders, new files, deleted files, deleted folders, and modified files.

            list[dict]: A list of dictionaries containing the files and folders.
        """

        new_files , new_folders , deleted_files , deleted_folders , modified_files = [],[],[],[],[]

        local_content = local_folders.get(folder,{}).get('content',[])

        remote_content = set(remote_folders.get(folder,{}).get('content',[]))


        for name in local_content:

            path = os.path.join(folder,name)

            if local_folders.get(path,{}).get('isdir',False):
                
                if name not in remote_content:
                    
                    new_folders.append(local_folders[path])

                else:
                     
                    remote_content.remove(name)

                new_folders_ , new_files_ , deleted_files_ , deleted_folders_ , modified_files_ = _compare_folder(path)

                new_folders.extend(new_folders_)
                new_files.extend(new_files_)
                deleted_files.extend(deleted_files_)
                deleted_folders.extend(deleted_folders_)
                modified_files.extend(modified_files_)

            else:

                if name not in remote_content:

                    new_files.append(local_files[path])

                else:

                    ids , modtime , size , version = (remote_files.get(path,{})).get('ids',[""]), (remote_files.get(path,{})).get('modtime',[]) , (remote_files.get(path,{})).get('size',[]) , (remote_files.get(path,{})).get('version',[1])

                    modtime_ , size_ , version_ = local_files[path]['modtime'] , local_files[path]['size'] , local_files[path]['version']

                    if modtime not in modtime_ or size not in size_ :

                        local_files[path]['version'] = version[-1] + 1

                        local_files[path]['other_version'] = dict(zip(version,ids))

                        modified_files.append(local_files[path])

                    else:

                        m = modtime.index(modtime_)
                        s = size.index(size_)

                        if m == s:

                            local_files[path]['version'] = version[m]

                        else:

                            local_files[path]['version'] = version[-1] + 1

                    

                        modified_files.append(local_files[path])


        deleted_folders = [remote_folders.get(os.path.join(folder,name),None) for name in remote_content if remote_folders.get(os.path.join(folder,name),None)]

        deleted_files = [remote_files.get(os.path.join(folder,name),None) for name in remote_content if remote_folders.get(os.path.join(folder,name),None)]


        return new_folders,new_files,deleted_files,deleted_folders,modified_files
        

    return _compare_folder(backup_folder_path)