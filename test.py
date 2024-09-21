from backend import remote
import json

from worker.cmd.indexer import operations

from backend.gdrive.modules import requests

# a = remote.ls()

# for i in a :
#     print(i)

a = operations.locals.indexer('./')
with open('tests/data/response_local.json','w') as file:
    json.dump(a,file)


print(a['.']['content'].keys())