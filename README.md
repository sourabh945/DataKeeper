# bizbackup-clt
This is a program which use to backup the file to the google drive using google drive api


-----------------------------------------------------------------------------------------

output:

py main.py
[Loading] Configurations ...
Choose the configuration which are you using and enter 0 for making new configuration : 

[1] default
> 1
[Done] Configurations
[Loading] access tokens...
[Done] access tokens
Path of backup forlder is ./backend

[Indexing] Both sources... 
[Done] Indexing
[Comparing] Both sources...
[Done] Comparing
-------------------------------------------------------------------
[Results]

Total number of folder in local: 19
Total number of files in local: 17
Total number of folder in remote: 0
Total number of files in remote: 0

-------------------------------------------------------------------

Total number of new folders: 11
Total number of new files: 25
Total number of deleted folders: 0
Total number of deleted files: 0
Total number of modified files: 0
-------------------------------------------------------------------

Choose the operation :

[1] For upload only
[2] For download only
[3] For upload and then download
[4] For cancel.

> 1

[Creating] Folders...
[creating] ./backend/gdrive
[done] ./backend/gdrive
[creating] ./backend/__pycache__
[done] ./backend/__pycache__
[creating] ./backend/gdrive/_secrets_
[done] ./backend/gdrive/_secrets_
[creating] ./backend/gdrive/modules
[done] ./backend/gdrive/modules
[creating] ./backend/gdrive/commands
[done] ./backend/gdrive/commands
[creating] ./backend/gdrive/__pycache__
[done] ./backend/gdrive/__pycache__
[creating] ./backend/gdrive/_secrets_/__pycache__
[done] ./backend/gdrive/_secrets_/__pycache__
[creating] ./backend/gdrive/modules/__helper__
[done] ./backend/gdrive/modules/__helper__
[creating] ./backend/gdrive/modules/__pycache__
[done] ./backend/gdrive/modules/__pycache__
[creating] ./backend/gdrive/modules/__helper__/__pycache__
[done] ./backend/gdrive/modules/__helper__/__pycache__
[creating] ./backend/gdrive/commands/__pycache__
[done] ./backend/gdrive/commands/__pycache__

[Done] creating folders

[Uploading] files...
[ Uploading ] file: ./backend/gdrive/_secrets_/__pycache__/__init__.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/_secrets_/__pycache__/gdrive_credentials.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/_secrets_/__init__.py
[ Uploading ] file: ./backend/gdrive/_secrets_/gdrive_credentials.py
[ Uploading ] file: ./backend/gdrive/modules/__helper__/__pycache__/mimetypes.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/modules/__helper__/mimetypes.py
[ Uploading ] file: ./backend/gdrive/modules/__pycache__/tokenizer.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/modules/__pycache__/error.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/modules/__pycache__/__init__.cpython-312.pyc
[ Done ] file: ./backend/gdrive/modules/__pycache__/tokenizer.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/modules/__pycache__/request.cpython-312.pyc
[ Done ] file: ./backend/gdrive/_secrets_/__pycache__/gdrive_credentials.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/modules/error.py
[ Done ] file: ./backend/gdrive/_secrets_/gdrive_credentials.py
[ Uploading ] file: ./backend/gdrive/modules/tokenizer.py
[ Done ] file: ./backend/gdrive/modules/__helper__/__pycache__/mimetypes.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/modules/__init__.py
[ Done ] file: ./backend/gdrive/modules/__pycache__/error.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/modules/request.py
[ Done ] file: ./backend/gdrive/_secrets_/__init__.py
[ Uploading ] file: ./backend/gdrive/commands/__pycache__/cmd.cpython-312.pyc
[ Done ] file: ./backend/gdrive/_secrets_/__pycache__/__init__.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/commands/__pycache__/__init__.cpython-312.pyc
[ Done ] file: ./backend/gdrive/modules/__pycache__/__init__.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/commands/cmd.py
[ Done ] file: ./backend/gdrive/modules/__helper__/mimetypes.py
[ Uploading ] file: ./backend/gdrive/commands/__init__.py
[ Done ] file: ./backend/gdrive/modules/error.py
[ Uploading ] file: ./backend/gdrive/__pycache__/__init__.cpython-312.pyc
[ Done ] file: ./backend/gdrive/modules/__pycache__/request.cpython-312.pyc
[ Uploading ] file: ./backend/gdrive/__pycache__/__scopes__.cpython-312.pyc
[ Done ] file: ./backend/gdrive/modules/tokenizer.py
[ Uploading ] file: ./backend/gdrive/__init__.py
[ Done ] file: ./backend/gdrive/modules/__init__.py
[ Done ] file: ./backend/gdrive/modules/request.py
[ Uploading ] file: ./backend/gdrive/.gitignore
[ Uploading ] file: ./backend/gdrive/__scopes__.py
[ Done ] file: ./backend/gdrive/commands/__pycache__/__init__.cpython-312.pyc
[ Uploading ] file: ./backend/__pycache__/__init__.cpython-312.pyc
[ Done ] file: ./backend/gdrive/commands/__init__.py
[ Uploading ] file: ./backend/__init__.py
[ Done ] file: ./backend/gdrive/commands/__pycache__/cmd.cpython-312.pyc
[ Done ] file: ./backend/gdrive/commands/cmd.py
[ Done ] file: ./backend/gdrive/__pycache__/__scopes__.cpython-312.pyc
[ Done ] file: ./backend/gdrive/__pycache__/__init__.cpython-312.pyc
[ Done ] file: ./backend/gdrive/__init__.py
[ Done ] file: ./backend/gdrive/.gitignore
[ Done ] file: ./backend/__pycache__/__init__.cpython-312.pyc
[ Done ] file: ./backend/__init__.py
[ Done ] file: ./backend/gdrive/__scopes__.py

[Done] uploading files
