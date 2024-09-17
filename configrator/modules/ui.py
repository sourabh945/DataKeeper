import os


### local imports ##################################

from backend.gdrive import tokenizer
from ...paths import token_path
from .__helper__.hide_folder import hide_folder



######################################################



##################################################################

def initizer_ui() -> dict[dict]:
    
    print("\nhello !!! There is no config.ini file in the folder config. For making config please answer these questions.\n")

    print('Please enter the path of the folder you wanted to backup. ')
    
    while True:

        local_folder = input(" > ")
        if os.path.isdir(local_folder):
            break
        else:
            print("Please select a valid folder.")

    print('folder selected.')

    print("Now the login open the browser and past the link( or it will happend automatically). And login with the gmail and password to give the permission to access the google drive.")
    print("Fell free to do this i the token is stored in the your computer in this current directory as in folder tokens/.\n")

    if not os.path.isdir(os.path.dirname(token_path)):
        os.mkdir(os.path.dirname(token_path))

    token = tokenizer()

    hide_folder(os.path.dirname(token_path))


    if token:

        print('\nSuccessfully logged in.\n')


    