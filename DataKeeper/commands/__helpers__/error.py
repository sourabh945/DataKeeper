def error(msg:str,exit_:bool=False,code:int=1):
    print(f'[ Erorr]  {msg} ')
    if exit_:
        exit(code)