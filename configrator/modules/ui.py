import os


### local imports ##################################

from ...backend import tokenizer
from .error import error


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

    if local_folder[-1] != '/':
        local_folder += "/"

    print('folder selected.')

    """ there i have to add to select between different drive when i make the  backend for them"""

    print("Now the login open the browser and past the link( or it will happend automatically). And login with the gmail and password to give the permission to access the google drive.")
    print("Fell free to do this i the token is stored in the your computer in this current directory as in a hidden folder tokens/.\n")

    token = True if tokenizer() else False # create the token 

    if token:

        print('\nSuccessfully logged in.\n')

    else:

        error("\nUnsuccessful login.\n")
    

    return local_folder,token





    