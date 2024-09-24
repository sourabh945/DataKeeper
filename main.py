print('[Loading] Configurations ...')

from paths import *

print('[Done] Configurations')

print('[Loading] access tokens...')

from backend import tokenizer , remote 

print('[Done] access tokens')

from commands import remote_list_2_dict, remote_ls , local_ls , write_tree , compare , load_tree

from runner import run 


## globals ##

tree = {}

local_folder , local_files , remote_folders , remote_files= {} , {} , {} , {}


def upload(folders:list,files:list,modified_files:list):

    print('[Creating] Folders...')

    _new_folders = run(remote.functions._create_folder,folders)
    
    print('[Done] Creating folders...')

    


if __name__ == '__main__':

    print("[Indexing] Both sources... ")

    ROOT_ID = remote.root_id()

    tree = load_tree(tree_path)

    local_folders, local_files = local_ls(folder_path,tree)

    lists = remote_ls()

    remote_dict = remote_list_2_dict(lists)

    remote_folders, remote_files = remote_ls(remote_dict,ROOT_ID)

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

