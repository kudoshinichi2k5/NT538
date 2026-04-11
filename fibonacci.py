import multiprocessing
import time

q = 1
arr = []

memo = {}

def _fib(k):
    if k == 0:
        return (0, 1)
    
    if k in memo:
        return memo[k]
    
    a, b = _fib(k >> 1)
    c = (a * ((b << 1) - a)) % q    
    d = (a * a + b * b) % q
    
    if k & 1:
        res = (d, (c + d) % q)
    else:
        res = (c, d) 
    memo[k] = res
    return res

def fibonacci(n):
    if n <= 1:
        return n % q
    return _fib(n)[0]

def func(bounds):
    start, end = bounds
    
    return [fibonacci(arr[i]) for i in range(start, end)]

def MAIN(input_file_path):
    global arr, q

    with open(input_file_path, "r") as f:
        data = f.read().split()

        n = int(data[0])
        q = int(data[1])

        arr = [int(x) for x in data[2:]]

    num_cores = 2
    chunk_size = (n + num_cores - 1) // num_cores

    bounds = []
    for i in range(num_cores):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, n)
        if start < end:
            bounds.append((start, end))

    with multiprocessing.Pool(num_cores) as p:
        results = p.map(func, bounds)

    final_results = []
    for res in results:
        final_results.extend(res)

    return final_results  
    
if __name__ == "__main__":
    start = time.perf_counter()
    # print(MAIN("test1_basic.txt"))
    print(MAIN("test2_maxN_smallA.txt"))
    # print(MAIN("test3_smallN_maxA.txt"))
    # print(MAIN("test4_ultimate.txt"))
    # print(MAIN("test5_edge_cases.txt"))


    end = time.perf_counter()
    print("Thoi gian chay: ", end - start)