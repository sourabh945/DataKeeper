import os
import re
import json


from .__helper__.hide_folder import hide_folder
from .__helper__.error import error

CONFIG_PATH = './config/'

def is_valid_folder_name(name):
    """Checks if the name is valid for a folder.

    For simplicity, we'll only allow alphanumeric characters, underscores, 
    hyphens, and spaces. You can adjust the regex for stricter or more 
    lenient rules.
    """
    regex = r"^[a-zA-Z0-9_ -]+$"
    match = re.match(regex, name)
    return bool(match)

def create_config():
    """Creates a new configuration folder.

    This function prompts the user for a name for the configuration and then
    creates a hidden folder with that name.
    """

    try:
        if not os.path.isdir(CONFIG_PATH):
            os.mkdir(CONFIG_PATH)
        hide_folder(CONFIG_PATH)

        print('Hello !!!\n')
        print("Please enter a name for the configuration:\n")

        while True:
            name = input('> ')
            if is_valid_folder_name(name) and not os.path.isdir(os.path.join(CONFIG_PATH, name)):
                break
            else:
                print("Invalid folder name. Please use only letters, numbers, spaces, underscores, or hyphens.")
                print("And this folder might be already exits so try another name.")

        print(f'\nOkay, creating a hidden folder for this configuration: {name}')

        try:
            os.mkdir(os.path.join(CONFIG_PATH, name))  # Safer path joining
        except OSError as e:
            error(f"Error creating folder: {e}")
            # Handle the error appropriately (e.g., log it, exit the program)

        print('\nEnter the path of the folder backup >')

        while True:
            folder = input('> ')
            if os.path.isdir(folder) :
                break 
            else:
                print('\nPlease enter the path of a valid folder')

        folder = folder.rsplit('/')[0]

        with open(os.path.join(CONFIG_PATH,name,'config.json'),'w') as file:
            json.dump({'backup_folder':folder},file)

        return name,folder


    except Exception as err:
        error(err)