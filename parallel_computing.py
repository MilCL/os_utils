import os
import multiprocessing as mp
import numpy as np
import time


""" #multiprocessing library 
1 - Pool Class
        A - Synchronous execution
            Pool.map() and Pool.starmap()
            Pool.apply()
        B - Asynchronous execution
            Pool.map_async() and Pool.starmap_async()
            Pool.apply_async())
2 - Process Class """


#Processes vs threads

#Processes: running in isolate memory locations

############################## Multiprocessing #############################################################



#2 modes synchronous and asynchronous execution
#Synchronous execution : the processes are completed in the same order in which it was started (requires to use a lock)
#Asynchronous : no locking required, a bit faster but the results gets mixed up


#################################### example 1 #######################################################

#https://www.machinelearningplus.com/python/parallel-processing-python/
#Goal: counting numbers in range for each row 


#Non parallel code
def howmany_within_range(row, minimum = 4, maximum = 8, index = None):
    """
    Returns how many numbers lie within `maximum` and `minimum` in a given `row`
    """

    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    
    if index is not None:
        return (index, count)
    else :
        return count

#Callback function to collect asynchronous code result
def collect_result(result):
    global results
    results.append(result)



if __name__ == '__main__' :

    # Prepare data
    np.random.RandomState(100)
    arr = np.random.randint(0, 10, size=[200, 5])
    data = arr.tolist()


    #Non parallel version
    start = time.time()
    results = []
    for row in data:
        results.append(howmany_within_range(row, minimum=4, maximum=8))
        pass
    end = time.time()
    print('1 - Non parallel script took', end - start, 's')
    print(results[:10])


    #Number of parallel processes that can run on the machine
    print("Number of processors: ", mp.cpu_count())


    #Parallelized version

    # 1 - Parallelizing using Pool.apply() (apply allows to pass arguments to the function)
    start = time.time()
    # Step 1: Init multiprocessing.Pool()
    pool = mp.Pool(mp.cpu_count())
    results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]
    # Step 3: Don't forget to close
    pool.close()    

    end = time.time()
    print('2 - Parallel pool apply took', end-start, 's') 
    print(results[:10])





    # 2 - Parallelizing using Pool.map() (map allows to pass an iterable)
    start = time.time()
    pool = mp.Pool(mp.cpu_count())
    results = pool.map(howmany_within_range, [row for row in data])
    # Step 3: Don't forget to close
    pool.close()    

    end = time.time()
    print('2 - Parallel pool map took', end-start, 's') 


    # 3 - Parallelizing using startmap (like map but allows to give several arguments)
    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap(howmany_within_range, [(row, 4, 8) for row in data])
    pool.close()


    ############################################ Asynchronous processing #####################################

    #1 - Using apply (warning, result arrives in disorder). Requires a callback function to say how to store the result
    start = time.time()
    pool = mp.Pool(mp.cpu_count())
    results = []
    for i, row in enumerate(data):
        pool.apply_async(howmany_within_range, args=(row, 4, 8, i), callback=collect_result)

    #Close Pool and let all the processes complete    
    pool.close()

    #Postpones the execution of next line of code until all processes in the queue are done.
    pool.join()  

    # Sort results [OPTIONAL]
    print(results[:10])
    results.sort(key=lambda x: x[0])
    results_final = [r for i, r in results]
    end = time.time()
    print('Asynch code took', end-start, 's')
    print(results_final[:5])


    #Apply without callback (using .get())
    
    pool = mp.Pool(mp.cpu_count())

    results_objects = [pool.apply_async(howmany_within_range, args=(row, 4, 8, i)) for i, row in enumerate(data) ]

    result = [r.get() for r in results_objects]

    pool.close()
    pool.join()  

    print(results[:10])
    results.sort(key=lambda x: x[0])
    results_final = [r for i, r in results]
    end = time.time()
    print('Asynch code took', end-start, 's')
    print(results_final[:5])