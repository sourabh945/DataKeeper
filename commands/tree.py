from ..paths import tree_path

import json

def write_tree(local_folder:dict,local_files:dict) -> None:

    with open(tree_path,'w') as files:

        json.dump({**local_folder,**local_files},files)

def load_tree() -> dict:

    with open(tree_path,'r') as files:

        return json.load(files)