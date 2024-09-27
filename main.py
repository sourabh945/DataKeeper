print('[Loading] Configurations ...')

from paths import *

print('[Done] Configurations')

print('[Loading] access tokens...')

from backend import tokenizer , remote 

print('[Done] access tokens')

from commands import remote_ls , local_ls , remote_list_2_dict , find_folder_id_in_root as folder_id_find_in_root


from runner import run ,async_run


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


def upload(tree:dict,upload_files:list):
   
    fails = []

    print('\n[Creating] Folders...')


    local__ , ids = async_run(remote.create_folder,tree)

    print('\n[Done] creating folders')

    for item in upload_files:
       
       if not item['parents'] :
           
            item['parents'] = [ids.get(item['path'],[])]

    print('\n[Uploading] files...')

    results = run(remote.functions._upload_file,upload_files)

    print('\n[Done] uploading files')

    return results, fails



if __name__ == '__main__':

    print("[Indexing] Both sources... ")

    ROOT_ID = remote.root_id()

    lists = remote.ls()

    lists = remote_list_2_dict(lists)

    backup_folder_id = folder_id_find_in_root(lists,ROOT_ID,os.path.basename(folder_path))


    if not backup_folder_id:

        backup_folder_id = remote.create_folder(os.path.basename(folder_path),ROOT_ID)

        if not backup_folder_id:

            print('Unable to create folders in remote')
            
            exit(1)

        lists = remote.ls()

        lists = remote_list_2_dict(lists)

    

    remote_folders , remote_files = remote_ls(lists,backup_folder_id,folder_path)

    ################################################33

    import json

    with open(tree_path,'w') as files:

        json.dump({**remote_folders,**remote_files},files)

    ##################################################3

    print('[Done] Indexing')
    print('[Comparing] Both sources...')

    local_ , upload_files, deleted_folders , deleted_files , count_new_folders , count_new_files , count_modified_files ,total_folders,total_files= local_ls(folder_path,backup_folder_id,ROOT_ID,remote_folders,remote_files)

    print('[Done] Comparing')

    print('-------------------------------------------------------------------\n[Results]\n')

    print(f"Total number of folder in local: {total_folders}")
    print(f"Total number of files in local: {total_files}")

    print(f"Total number of folder in remote: {len(remote_folders)}")
    print(f"Total number of files in remote: {len(remote_files)}")

    print('-------------------------------------------------------------------\n')

    print(f"Total number of new folders: {count_new_folders}")
    print(f"Total number of new files: {count_new_files}")

    print(f"Total number of deleted folders: {len(deleted_folders)}")
    print(f"Total number of deleted files: {len(deleted_files)}")

    print(f"Total number of modified files: {count_modified_files}")




    print("-------------------------------------------------------------------\n")

    if sum([len(deleted_files),len(deleted_folders),count_modified_files,count_new_files,count_new_folders]) == 0:

        print('Every thing is up to date ')

        exit(0)

    print('Choose the operation :\n')

    print("[1] For upload only")
    print("[2] For download only")
    print("[3] For upload and then download")
    print('[4] For cancel.\n')

    option = int(input("> "))

    while option < 1 or option > 4:
        print("choose the correct option. \n")
        option = int(input("> "))

    if option == 1 and sum([count_modified_files,count_new_files]) > 0 :

        # print(upload_files)

        result , fail = upload(local_,upload_files)

        for i in result:

            if result[i]:
                fail.append(i)

        print(f'No. of fails:{len(fail)}')


    elif option == 2 and len(deleted_folders)+len(deleted_files) > 0:

        donwloads(deleted_folders,deleted_files)

    elif option == 3:

        upload(local_,upload_files)

        donwloads(deleted_folders,deleted_files)


    elif option == 4:

        print('Cancelling every thing')

        exit(0)

    

