import os

def get_size(path):
    try:
        os.path.getsize(path)
    except:
        return -1