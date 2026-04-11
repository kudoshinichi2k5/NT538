import multiprocessing
import time 

arr = []

def func(bounds):
    start, end = bounds
    return sum([int(x) for x in arr[start:end] if x > 0 and x % 3 == 0])

def MAIN(input_file_path):
    global arr

    with open(input_file_path, "r") as f:
        n = int(f.readline())   
        arr = list(map(float, f.readline().split()))

    num_cores = 2
    chunk_size = (n + num_cores - 1) // num_cores

    bounds = []
    for i in range(num_cores):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, n)
        if start < end:
            bounds.append((start, end))

    with multiprocessing.Pool(num_cores) as p:
        total_sum = sum(p.map(func, bounds))

    return total_sum

if __name__ == '__main__':
    start = time.perf_counter()
    print(MAIN("input.txt"))

    end = time.perf_counter()
    print("Thoi gian chay: ", end - start)