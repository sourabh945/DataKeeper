import json
import os 

### local imports ####################################

from .error import error
from ...paths import config_path,tree_path
from .ui import initizer_ui
from .hide_folder import hide_folder

######################################################

def configurator():

    try:

        if not os.path.isdir(os.path.dirname(config_path)):
            os.mkdir(os.path.dirname(config_path))

            hide_folder(os.path.dirname(config_path))
        
            backup_folder,_ = initizer_ui()

            with open(config_path,'w') as file:
                json.dump({'backup_folder':backup_folder},file)

        else:

            if os.path.isfile(config_path):
                with open(config_path,'r') as file:
                    config = json.load(file)
                    return config
            else:
                backup_folder,_ = initizer_ui()

                with open(config_path,'w') as file:
                    json.dump({'backup_folder':backup_folder},file)
        
        try:
            with open(tree_path,'r') as file:
                tree = json.load(file)
        except:
            tree = {}

        return backup_folder , tree


    except Exception as err:

        error(err,exit_=True)

######################################################