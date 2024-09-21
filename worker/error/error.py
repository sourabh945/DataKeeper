def error(message:str,exit_:bool=False,code:int=1) -> None:
    print(f'[ Error ] {message}')
    if exit_:
        exit(code)