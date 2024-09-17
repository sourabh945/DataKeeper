from .backend import remote

from .backend.gdrive.modules import requests

print(requests.ls(q='trashed=false',fields='files(id,name)').get('files',[]))

print(
    '\n'
)

print(remote.ls())