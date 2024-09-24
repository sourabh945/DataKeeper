print('[Loading] Configurations ...')

from paths import *

print('[Done] Configurations')

print('[Loading] access tokens...')

from backend import tokenizer , remote 

print('[Done] access tokens')

from commands import remote_list_2_dict, remote_ls , local_ls , write_tree , compare , load_tree , folder_id_in_root

from runner import run 


## globals ##

tree = {}

local_folder , local_files , remote_folders , remote_files= {} , {} , {} , {}

####################################################################################

def donwloads(folders:dict,files:dict):

    print('[Creating] Folder in locals...')

    for item in folders:

        if not os.path.isdir(item['path']):

            os.mkdir(item['path'])

    print('[Done] Creating.')

    print('[Donwloading] files...')

    run(remote.functions._download_file,files)

    print('[Done] Donwloading.')


def write_to_locals(folders:dict,files:dict,modified_files:dict):

    print("[Processing] Files upload outputs ...")

    for item in folders.keys():

        local_folder[item]['id'] = folders[item]

    for item in files.keys():

        local_files[item]['id'] = files[item]

    for item in modified_files.keys():

        local_files[item]['id'] = modified_files[item]

        local_files[item]['version'] += 1

    print('[Done] processing.')


def upload(folders:list,files:list,modified_files:list):

    print('[Creating] Folders...')

    _new_folders = run(remote.functions._create_folder,folders)
    
    print('[Done] Creating folders...')

    for item in files:
        if os.path.dirname(item['path']) in _new_folders.keys():
            item['parents'] = [_new_folders[os.path.dirname(item)]]

    print('[Uploading] new_files ..,')

    _new_files = run(remote.functions._upload_file,files)

    print('[Done] uploading new files.')

    print('[Uploading] modified files...')

    _modified_files = run(remote.functions._upload_file,modified_files)

    print('[Done] uploading modified files.')

    write_to_locals(_new_folders,_new_files,_modified_files)

    return _new_folders , _new_files , _modified_files


    


if __name__ == '__main__':

    print("[Indexing] Both sources... ")

    ROOT_ID = remote.root_id()

    tree = load_tree(tree_path)

    local_folders, local_files = local_ls(folder_path,tree)

    lists = remote.ls()

    remote_dict = remote_list_2_dict(lists)

    _folder_id = folder_id_in_root(remote_dict,os.path.basename(folder_path),ROOT_ID)

    if not _folder_id:

        _folder_id = remote.create_folder(os.path.basename(folder_path),ROOT_ID)

    remote_folders, remote_files = remote_ls(remote_dict,_folder_id,folder_path)

    print('[Done] Indexing')

    print('-------------------------------------------------------------------\n[Results]\n')

    print(f"Total number of folder in local: {len(local_folders)}")
    print(f"Total number of files in local: {len(local_files)}")

    print(f"Total number of folder in remote: {len(remote_folders)}")
    print(f"Total number of files in remote: {len(remote_files)}")

    print('-------------------------------------------------------------------\n[Comparing]\n')

    print(f"Comparing local and remote folders...")

    print(f"Comparing local and remote files...")

    new_folders, new_file , deleted_folders , deleted_files , modified_files = compare(local_folders,remote_folders,local_files,remote_files)

    print('[Done] Comparing')

    print('-------------------------------------------------------------------\n[Results]\n')

    print(f"Total number of new folders: {len(new_folders)}")
    print(f"Total number of new files: {len(new_file)}")

    print(f"Total number of deleted folders: {len(deleted_folders)}")
    print(f"Total number of deleted files: {len(deleted_files)}")

    print(f"Total number of modified files: {len(modified_files)}")


    print("-------------------------------------------------------------------\n")

    print('Choose the operation :\n')

    print("[1] For upload only")
    print("[2] For download only")
    print("[3] For upload and then download")
    print('[4] For cancel.\n')

    option = int(input("> "))

    while option < 1 or option > 4:
        print("choose the correct option. \n")
        option = int(input("> "))

    if option == 1:

        upload(new_folders,new_file,modified_files)

        print('[Writting] tree')

        write_tree(local_folder,local_files,tree_path)

        print('[Done] writting')


    elif option == 2:

        donwloads(deleted_folders,deleted_files)

    elif option == 3:

        upload(new_folders,new_file,modified_files)

        donwloads(deleted_folders,deleted_files)

        print('[Writting] tree')

        write_tree(local_folder,local_files,tree_path)

        print('[Done] writting')


    elif option == 4:

        pass

    

