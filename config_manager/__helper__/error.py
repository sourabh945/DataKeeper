

def error(message:str,exit_:bool=True,code:int=1) -> None:
    """this function print the error"""
    print(f'Error: {message}')
    if exit_:
        exit(code)