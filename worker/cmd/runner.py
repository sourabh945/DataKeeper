import multiprocessing as mp 
import queue 

### local import ###############################


################################################



CPU_COUNT = mp.cpu_count()

WORKERS = 2*CPU_COUNT+1


###############################################


def _runner(func,queue,message,message_complete,message_fails,**kwargs):

    result = func(**kwargs)

    if result:

        queue.put([message,result])
        print(message_complete+message)

    elif not result:

        queue.put([message,result])
        print(message_fails+message)

    


def runner(func,list_of_kwargs:list,message_start:str=None,message_complete:str=None,message_fails:str=None,message_iterate:list=[]):
    """
    it runs the given function using multiprocess pool with apply_async method and return the result """

    result = queue.Queue()

    print("Process started")

    with mp.Pool(WORKERS) as pool:

        for message,kwargs in zip(message_iterate,list_of_kwargs):

            print(message_start+message)

            pool.apply_async(_runner,args=(func,result,message,message_complete,message_fails),kwds=kwargs)

        

    pool.close()

    pool.join()

    print("Process finished")

    res = []

    while not result.empty():

        res.append(result.get())

    return res

