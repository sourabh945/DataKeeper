import os 
import datetime 

from backend import remote

from ..error import error


class operations:

    class __helper__:

        def get_modtime(path:str) -> str:

            last_modified_timestamp = os.path.getmtime(path)
            last_modified = datetime.datetime.fromtimestamp(last_modified_timestamp)

            dt_utc = last_modified.astimezone(datetime.timezone.utc)

            last_modified_iso = dt_utc.isoformat()[:-9] + 'Z'

            return last_modified_iso
        
    class commans:

        def search_tree(tree:dict,path:str) -> dict:
            
            if not tree or not path:
                error('Tree or path is empty.')
                return {}
            
            tree_ = tree.copy()
            
            path_list = [ i for i in path.split('/') if i != " " or i != "" ]

            last = path_list.pop(-1)

            while path_list :

                folder = path_list.pop(0)

                try:
                    tree_ = tree_[folder]


    class locals:

        def _indexer(path:str) -> dict:

            result = {}

            for i in os.listdir(path):
                if os.path.isdir(f'{path}/{i}'):

                    result[i] = {
                        "path":f'{path}/{i}',
                        "isdir":True,
                        "id":None,
                        "parents":None,
                        "version":None,
                        "content":operations.locals._indexer(f'{path}/{i}')
                    }
                else:

                    result[i] = {
                        "path":f'{path}/{i}',
                        "isdir":False,
                        "size":os.path.getsize(f'{path}/{i}'),
                        "modtime": operations.__helper__.get_modtime(f'{path}/{i}'),
                        "id":None,
                        "parents":None,
                        "version":None
                    }
                    
            return result
        
        def indexer(path:str) -> str:

            path = path.rsplit("/",maxsplit=1)[0]

            return {
                path:{
                    "path":f'{path}',
                    "isdir":True,
                    "id":None,
                    "parents":None,
                    "version":None,
                    "content":operations.locals._indexer(f'{path}')
                }
            }




    class remote:

        def _indexer(listDir:list[dict],parent_id:str,folder_string:str) -> dict:

            result = {}

            listDir2 = listDir.copy()


            for item in listDir:

                if parent_id in item.get('parents',[]):
                    if item['mimeType'] == "application/vnd.google-apps.folder":
                        listDir2.remove(item)
                        result[item['name']]={
                                'path':f"{folder_string}/{item["name"]}",          
                                'id':item['id'],
                                'parents':parent_id,
                                'isdir':True,
                                'content':operations.remote._indexer(listDir2,item['id'],f"{folder_string}/{item['name']}")
                            }
                    else:
                        listDir2.remove(item)
                        result[item['name']]={
                                'path':f"{folder_string}/{item['name']}",          
                                'id':item['id'],
                                'parents':parent_id,
                                'isdir':False,
                                'size':item['size'],
                                'modtime':item['modifiedTime']
                            }
            return result 
        
        def indexer(listDir:list[dict],folder_id:str,parent_id:str,folder_string:str) -> dict:

            folder_string = folder_string.rsplit("/")

            return {
                folder_string:{
                    'path':f'{folder_string}',
                    'id':folder_id,
                    'parents':parent_id,
                    'isdir':True,
                    'content':operations.remote._indexer(listDir,parent_id,folder_string)
                }
            }


        def remote_indexer() -> dict:

            ROOT_ID = remote.root_id()

            return {'root#':{
                'path':'root#',
                'id':ROOT_ID,
                'parents':[],
                'isdir':True,
                'content':operations.remote._indexer(remote.ls(),ROOT_ID,'root#')
            }}
