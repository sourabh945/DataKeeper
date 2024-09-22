
from functools import wraps
import os

### google api imports ########################

from googleapiclient.errors import HttpError

###############################################

def error(message:str,exit_:bool=False,code:int=1) -> None:
    """
    Prints an error message and optionally exits the program.

    Args:
        message (str): The error message to print.
        exit_ (bool, optional): Whether to exit the program after printing the error. Defaults to False.
        code (int, optional): The exit code to use if exit_ is True. Defaults to 1.
    """
    print(f'[ Error ] {message}')
    print(f'\nPlease raise issue to this https://github.com/sourabh945/bizbackup-clt/issues if unable to resolve the issue.')
    if exit_:
        exit(code)


##################################################

### decorators for error handling ##########################

def httperrors(func):
    """
    Decorator to handle HttpError exceptions from Google API calls.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The decorated function.
    """
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except HttpError as err:
            message = f' [ {err.status_code} ] [ {err.uri} ]\n {err._get_reason()}'
            error(message)
            return None
    return wrapper


################################################################

def is_exists(func):
    """
    Decorator to check if a file exists before proceeding.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The decorated function.
    """
    @wraps(func)
    def wrapper(*args,**kwargs):
        file_path = kwargs.get('path') or args[0]
        if os.path.isfile(file_path):
            return func(*args,**kwargs)
        else:
            error(f'file {file_path} not found')
            return None       
    return wrapper

def is_possible(func):
    """
    Decorator to check if a folder exists before proceeding.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The decorated function.
    """
    @wraps(func)
    def wrapper(*args,**kwargs):
        folder_path = os.path.split(kwargs['path'])
        if os.path.isdir(folder_path):
            return func(*args,**kwargs)
        else:
            error(f'folder {folder_path} not found')
            return None       
    return wrapper
