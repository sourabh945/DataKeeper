
import os 

from .__helpers__.time import get_modtime
from .__helpers__.trying import get_size


def lister(item) -> list:

    if 'list' in str(type(item)):
        return item 
    else:
        return [item]




def remote_list_2_dict(remote_list:list[dict]) -> dict[dict]:
    """This function take the list of remote and return a dict with parents as key and value are the 
    the list of all the content of the folder"""

    result = {}

    for item in remote_list:

        if item.get('parents',None):
        
            result[item['parents'][0]] = result.get(item['parents'][0],[])+[item]

    return result 


def find_folder_id_in_root(remote_dict,ROOT_ID,path):

    try:

        if path[-1] == '/':
            path = path[:-1]

        for item in remote_dict[ROOT_ID]:
            if item['name'] == os.path.basename(path):
                return item['id']

    except:
        return None


def remote_ls(remote_dict:dict,folder_id:str,path_string:str='./') -> list[dict]:


    res_folders , res = {} , {}

    def _indexer(parent_id,parent_path:str):

        content = remote_dict.get(parent_id,[])

        for item in content:

            path = os.path.join(parent_path,item['name'])

            if item['mimeType'] == 'application/vnd.google-apps.folder':

                res_folders[path] = {
                    'path':path,
                    'id':item['id'],
                    'isdir':True,
                    'parents':[parent_id],
                    'content':[i['name'] for i in remote_dict.get(item['id'],[])]
                }

                _indexer(item['id'],path)

            else:

                files = res.get(path,{})

                if files:

                    res[path]['id'] = lister(res[path]['id']) + [item['id']]
                    res[path]['version'] = lister(res[path]['version']) + lister(item.get('properties',{}).get('version',[1]))
                    res[path]['size'] = lister(res[path]['size']) + lister(item['size'])
                    res[path]['modtime'] = lister(res[path]['modtime']) + lister(item['modifiedTime'])
                    res[path]['other_version'][item['id']] = item.get('properties',{}).get('version',1)
                
                else:

                    res[path] = {
                        'path':path,
                        'id':[item['id']],
                        'isdir':False,
                        'parents':lister(parent_id),
                        'version':item.get('properties',{}).get('version',[1]),
                        'other_version':item.get('properties',{}).get('other_version',{item['id']:item.get('properties',{}).get('version',1)}),
                        'size':[item['size']],
                        'modtime':[item['modifiedTime']],
                    }

    _indexer(folder_id,path_string)

    return res_folders , res




def local_ls(path:str,folder_id:str,parent_id:str,_remote_folders:dict = {},_remote_files:dict={}) -> list[dict]:

    """Compares local files and folders with remote data and identifies new, modified, and deleted items.

    Args:
        path (str): The local path to scan.
        folder_id (str): The ID of the corresponding remote folder.
        parent_id (str): The ID of the parent remote folder.
        remote_folders (dict, optional): Dictionary of remote folders. Defaults to {}.
        remote_files (dict, optional): Dictionary of remote files. Defaults to {}.

    Returns:
        list[dict]: A tuple containing: local file/folder structure, list of files to upload, 
                     deleted folders, deleted files, counts of new folders/files/modifications,
                     total local folders, total local files.
    """

    upload_files = []
    
    local_ = {}

    def _indexer(path_:str,folder_id:str):

        count_new_folders = 0
        count_new_files = 0
        count_modified_files = 0
        total_folders = 0
        total_files = 0

        res = {}

        content = os.listdir(path_)

        for item in content:

            path = os.path.join(path_,item)

            if os.path.isdir(path):

                total_folders += 1

                if path in _remote_folders:

                    info = _remote_folders[path]

                    del _remote_folders[path]

                    index , cn ,cnf , cm , tf , tff = _indexer(path,info['id'])

                    count_new_folders += cn
                    count_new_files += cnf
                    count_modified_files += cm
                    total_folders += tff
                    total_files += tf


                    res[path] = {
                        'path':path,
                        'id':info['id'],
                        'isdir':True,
                        'parents':info['parents'],
                        'content': index ,
                    }

                else:

                    count_new_folders += 1

                    index , cn ,cnf, cm , tf , tff = _indexer(path,"")

                    count_new_folders += cn
                    count_new_files += cnf
                    count_modified_files += cm
                    total_files += tf
                    total_folders += tff



                    res[path] = {
                        'path':path,
                        'id':"",
                        'isdir':True,
                        'parents':[folder_id],
                        'content':index,
                    }

            else:

                total_files += 1

                if path in _remote_files:

                    info = _remote_files[path]

                    del _remote_files[path]

                    size, modtime  = get_size(path) , get_modtime(path)

                    if str(size) in lister(info['size']) and modtime in lister(info['modtime']):

                        pass

                    else:

                        count_modified_files += 1

                        dict = {
                            'path':path,
                            'id':"",
                            'isdir':False,
                            'parents':[folder_id],
                            'version':int(info['version'][-1]) + 1,
                            'other_version':info['other_version'],
                            'size':size,
                            'modtime':modtime,
                        }

                        upload_files.append(dict)

                else:

                    count_new_files += 1 

                    dict = {
                        'path':path,
                        'id':"",
                        'isdir':False,
                        'parents':[folder_id],
                        'other_version':{},
                        'version':1,
                        'size':get_size(path),
                        'modtime':get_modtime(path),
                    }

                    upload_files.append(dict)

        return res , count_new_folders , count_new_files , count_modified_files , total_folders , total_files

    res , count_new_folders , count_new_files , count_modified_files , total_folders , total_files = _indexer(path,folder_id)

    local_ = {
        'path':path,
        'id':folder_id,
        'isdir':True,
        'parents':[parent_id],
        'content':res,
    }

    return local_ , upload_files, _remote_folders , _remote_files , count_new_folders , count_new_files , count_modified_files , total_folders , total_files


