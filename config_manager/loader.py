
import os 
import json


from __helper__.error import error


CONFIG_PATH = './config/'


def load_config() -> list[str,str]:

    try:

        configs = os.path.listdir(CONFIG_PATH)

        if configs:

            print("Choose the configuration which are you using and enter 0 for making new configuration : \n")

            for i in configs:

                print(f'[{i+1}] {configs[i]}')

            config_index = int(input("> "))

            while config_index > len(config_index) or config_index < 0:
                print("Please enter a valid number.")
                config_index = int(input("> "))
            
            if config_index == 0 :

                return None
            
            else:

                try:

                    with open(os.path.join(configs[config_index-1],'config.json'),'r') as file:
                        folder = json.load(file)

                    return configs[config_index-1] , folder['backup_folder']
                
                except :

                    return None

    except Exception as err:
        
        error(err,exit_=False)

        return None