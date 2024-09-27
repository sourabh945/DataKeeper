import asyncio 
import os 

async def caller(func:callable,name:str,parent_id:str):

    if name[-1] == '/':
        name = name[:-1]

    print(f'[creating] {name}')

    name_ = os.path.basename(name)

    res = func(name_,parent_id)

    if res : 

        print(f'[done] {name}')

    else:

        print(f'[fail] {name}')

    return res


async def _runner(func:callable,names:list,parent_id:str):

    res = {}

    for i in names:

        r = await caller(func,i,parent_id)

        res[i] = r

    return res


async def _run(func:callable,local:dict):

    ids = {}

    parent_id = local['id']

    content = local['content']

    names = [i for i in content.keys() if content[i]['isdir'] and content[i]['id'] == ""]

    res = await _runner(func,names,parent_id)

    for i in res:
        content[i]['id'] = res[i]
        ids[i] = res[i]

    for item in content:

        if content[item]['isdir']:

            content[item]['content'] , _ids = await _run(func,content[item])

            ids = {**ids,**_ids}


    return content , ids


def async_run(func:callable,local:dict):

    content , ids = asyncio.run(_run(func,local))

    local['content'] = content

    return local , ids
