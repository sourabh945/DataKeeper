import os 
import datetime 



class operations:

    class __helper__:

        def get_modtime(path:str) -> str:

            last_modified_timestamp = os.path.getmtime(path)
            last_modified = datetime.datetime.fromtimestamp(last_modified_timestamp)

            dt_utc = last_modified.astimezone(datetime.timezone.utc)

            last_modified_iso = dt_utc.isoformat()[:-9] + 'Z'

            return last_modified_iso

    class locals:

        def _indexer(path:str) -> dict:

            result = []

            for i in os.listdir(path):
                if os.path.isdir(f'{path}/{i}'):

                    result.append(
                        {i:{
                        "path":f'{path}/{i}',
                        "isdir":True,
                        "id":None,
                        "parents":None,
                        "version":None,
                        "content":operations.locals._indexer(f'{path}/{i}')
                        }})
                else:

                    result.append(
                        {i:{
                        "path":f'{path}/{i}',
                        "isdir":False,
                        "size":os.path.getsize(f'{path}/{i}'),
                        "modtime": operations.__helper__.get_modtime(f'{path}/{i}'),
                        "id":None,
                        "parents":None,
                        "version":None
                        }})
                    
            return result
        
        def indexer(path:str) -> str:

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

        def _indexer(listDir:list[dict]) -> dict:

            pass

import json

print(json.dumps(operations.locals.indexer(".")))