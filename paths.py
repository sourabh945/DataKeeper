from config_manager import load_config , create_config

import os 

CONFIG_PATH = './config/'

if os.path.isdir(CONFIG_PATH):
    try:
        config_name  , folder_path = load_config()

    except:
        config_name , folder_path = create_config()
else:
    config_name, folder_path = create_config()


if folder_path[-1] == "/":
    folder_path = folder_path[:-1]


token_path = f"./config/{config_name}/token.json"

connfig_path = f"./config/{config_name}/config.json"

tree_path = f"./config/{config_name}/tree.json"

