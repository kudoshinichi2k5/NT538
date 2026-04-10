import multiprocessing
import time

q = 1
arr = []

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b
        a %= q
        b %= q
    return a

def func(bounds):
    arr_tmp = []
    start, end = bounds
    
    for i in range(start, end):
        res = fibonacci(arr[i])
        arr_tmp.append(res)
    
    return arr_tmp

def MAIN(input_file_path):
    global arr, q

    with open(input_file_path, "r") as f:
        first_line = f.readline().split()

        n = int(first_line[0])
        q = int(first_line[1])

        arr = [int(f.readline()) for _ in range(n)]

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
    print(MAIN("input.txt"))

    end = time.perf_counter()
    print("Thoi gian chay: ", end - start)