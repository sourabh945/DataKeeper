
def error(message:str,exit_:bool=True,code:int=1):
    print(message)
    if exit_:
        exit(code)