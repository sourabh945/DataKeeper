from backend import remote
import json

from backend.gdrive.modules import requests

# result = (requests.ls(q='trashed=false',fields='files(id,name,parents)').get('files',[]))

# print(
#     '\n'
# # )

# print(remote.ls())

# # print(requests.get(fileId='root',fields='id'))


from local import local

result = local.ls('./')

print('hello \n')


with open('tests/data/response.json','w') as file:
    json.dump(result,file)