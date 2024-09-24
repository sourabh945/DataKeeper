

def remote_list_2_dict(remote_list:list[dict]) -> dict[dict]:
    """This function take the list of remote and return a dict with parents as key and value are the 
    the list of all the content of the folder"""

    result = {}

    for item in remote_list:

        if not item.get('parents',None):
        
            result[item['parents'][0]] = result.get(item['parents'][0],[])+[item]

    return result 