

import json

def write_tree(local_folder:dict,local_files:dict,tree_path:str) -> None:

    with open(tree_path,'w') as files:

        json.dump({**local_folder,**local_files},files)

def load_tree(tree_path:str) -> dict:

    try:

        with open(tree_path,'r') as files:

            return json.load(files)
        
    except :
        return {}