
from functools import wraps

### google api imports ########################

from googleapiclient.errors import HttpError

###############################################

def error(message:str,exit_:bool=False,code:int=1) -> None:
    print(f'[ Error ] {message}')
    if exit_:
        exit(code)


##################################################

### decorators for error handling ##########################

def httperrors(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except HttpError as err:
            message = f' [ {err.status_code} ] [ {err.uri} ]\n {err._get_reason()}'
            error(message)
            return None
    return wrapper