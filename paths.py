from config_manager import load_config , create_config

import os 

CONFIG_PATH = './config'

if os.path.isdir(CONFIG_PATH):
    config_name  , folder_path = load_config()

    if config_name is None:
        config_name , folder_path = create_config()
else:
    config_name, folder_path = create_config()


token_path = f"./config/{config_name}/token.json"

connfig_path = f"./config/{config_name}/config.json"

tree_path = f"./config/{config_name}/tree.json"

