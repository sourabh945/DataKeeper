import multiprocessing as mp 
import queue

NUM_PROCESSES = 2*mp.cpu_count + 1

def run(func:callable,item_list:list) -> dict:

    res = queue.Queue()

    with mp.Pool(NUM_PROCESSES) as pool:

        for item in item_list:

            pool.apply_async(func,args=(item,res))

        pool.close()
        pool.join()

    result = {}

    while not res.empty():

        item = res.get()

        result[item[0]] = item[1]

    return result