import datetime 

import os

def get_modtime(path:str) -> str:

    try:

        last_modified_timestamp = os.path.getmtime(path)
        last_modified = datetime.datetime.fromtimestamp(last_modified_timestamp)

        dt_utc = last_modified.astimezone(datetime.timezone.utc)

        last_modified_iso = dt_utc.isoformat('T', timespec='milliseconds') + 'Z'

        return last_modified_iso
    
    except:
        return -1