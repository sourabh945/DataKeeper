
import os 

from .__helpers__.time import get_modtime
from .__helpers__.trying import get_size

def folder_id_in_root(remote_dict:dict,foldername:str,root_id:str) -> str:
   for item in remote_dict.get(root_id,{}):
      if item['name'] == foldername and item['mimeType'] == 'application/vnd.google-apps.folder':
         return item['id']

    



def local_ls(path:str,tree:dict[dict]={}) -> list[dict]:
    """
    Lists the files and folders in a given path.
    
    Args:
        path (str): The path to list.
        tree (dict[dict], optional): The tree of the files and folders. Defaults to {}.

    Returns:
        folders_ , files_

        list[dict]: A list of dictionaries containing the files and folders.
    """
    just_ = {}

    just_[path] = {
        
    }

    def _local_ls(path):

        folders_ ,files_ = {} , {}

        for item in os.listdir(path):

            if os.path.isdir(os.path.join(path,item)):
                
                _folders , _files = _local_ls(os.path.join(path,item))

                folders_[os.path.join(path,item)] = {
                    'path':os.path.join(path,item),
                    'isdir':True,
                    'id': (tree.get(os.path.join(path,item),{})).get('id',''),
                    'parents':(tree.get(os.path.join(path,item),{})).get('parents',[]),
                    'content': os.listdir(os.path.join(path,item))
                }

                folders_.update(_folders)

                files_.update(_files)

            else:
                files_[os.path.join(path,item)] = {
                    'path':os.path.join(path,item),
                    'id':(tree.get(os.path.join(path,item),{})).get('id',''),
                    'isdir':False,
                    'id':(tree.get(os.path.join(path,item),{})).get('id',""),
                    'parents':(tree.get(os.path.join(path,item),{})).get('parents',[]),
                    'version':(tree.get(os.path.join(path,item),{})).get('version',1),
                    'size':get_size(os.path.join(path,item)),
                    'modtime':get_modtime(os.path.join(path,item)),
                    'other_version':(tree.get(os.path.join(path,item),{})).get('other_version',{}),
                }

        return folders_,files_
    
    folders_ , files_ = _local_ls(path)

    folders_[path] = {
        'path':path,
        'isdir':True,
        'id': (tree.get(path,{})).get('id',''),
        'parents':(tree.get(path,{})).get('parents',[]),
        'content': os.listdir(path)
    }

    return folders_ , files_

def remote_ls(remote_dict:dict,folder_id:str,path_string:str='./') -> list[dict]:
    """
    Lists the files and folders in a given path.
    
    Args:
        path (str): The path to list.
        tree (dict[dict], optional): The tree of the files and folders. Defaults to {}.

    Returns:
        list[dict]: A list of dictionaries containing the files and folders.
    """

    def _indexer(parent_id,parent_path:str='.'):

        folders_ , files_ = {},{}

        for item in remote_dict.get(parent_path,[]):

            if item['mimeType'] == 'application/vnd.google-apps.folder':

                _folders , _files = _indexer(item['id'],os.path.join(parent_path,item['name']))

                folders_[os.path.join(parent_path,item['name'])] = {
                    'path':os.path.join(parent_path,item['name']),
                    'id':item['id'],
                    'isdir':True,
                    'parents':[parent_id],
                    'content':[i['name'] for i in remote_dict[item['id']]]
                }
                folders_.update(_folders)

                files_.update(_files)

            else:
                ids = files_.get(os.path.join(parent_path,item['name']),{}).get('id',[])
                versions = files_.get(os.path.join(parent_path,item['name']),{}).get('version',[])
                modtime = files_.get(os.path.join(parent_path,item['name']),{}).get('modtime',[])
                size = files_.get(os.path.join(parent_path,item['name']),{}).get('size',[])
                files_[os.path.join(parent_path,item['name'])] = {
                    'path':os.path.join(parent_path,item['name']) ,
                    'id':item['id'] + ids,
                    'isdir':False,
                    'parents':[parent_id],
                    'version':(item.get('properties',{}).get('version',[1])) + versions,
                    'size':list(item['size'])+size,
                    'modtime':list(item['modifiedTime'])+modtime,
                }

        return folders_,files_
    
    

    return _indexer(folder_id,path_string)


