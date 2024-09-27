import multiprocessing 
import queue

def printl(item,q):
    print(item)

NUM_PROCESSES = 2*(multiprocessing.cpu_count()) + 1

def run(func:callable,item_list:list) -> dict:

    with multiprocessing.Pool(NUM_PROCESSES) as pool:

        process = {}

        for item in item_list:

            pool.apply_async(func,args=(item,))

        pool.close()
        pool.join()

    # for i in process:

    #     process[i] = (process[i]).get()

    return process