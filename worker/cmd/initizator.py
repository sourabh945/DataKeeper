from ...backend import remote

import asyncio
import os

from runner import runner

ROOT_ID = remote.root_id()

def list_dir(name:str):

    result = []

    for i in os.listdir(name):
        if os.path.isdir(name+'/'+i) :
            result.append({i:list_dir(name+'/'+i)})
        else:
            result.append(i)
    return result

def indexer(local_path:str) -> dict:

    return {local_path:list_dir(local_path)}


