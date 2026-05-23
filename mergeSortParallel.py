import multiprocessing
import concurrent.futures

try:
    multiprocessing.set_start_method('fork', force=True)
except RuntimeError:
    pass

CPU_COUNT = multiprocessing.cpu_count()
DATA_GLOBAL = []

def merge(left, right):
    result = []
    append = result.append
    extend = result.extend

    i = j = 0
    len_l = len(left)
    len_r = len(right)

    while i < len_l and j < len_r:
        l = left[i]
        r = right[j]

        lv, ll = l
        rv, rl = r

        if lv > rv or (lv == rv and ll <= rl):
            append(l)
            i += 1
        else:
            append(r)
            j += 1

    if i < len_l:
        extend(left[i:])
    if j < len_r:
        extend(right[j:])

    return result

def sequential_merge_sort(data):
    n = len(data)

    if n <= 1:
        return data

    mid = n >> 1

    left = sequential_merge_sort(data[:mid])
    right = sequential_merge_sort(data[mid:])

    return merge(left, right)

def worker_sort(bounds):
    start, end = bounds
    return sequential_merge_sort(DATA_GLOBAL[start:end])

def parallel_merge_sort(n):
    if n < 5000:
        workers = 1
    elif n < 50000:
        workers = 4
    elif n < 200000:
        workers = min(8, CPU_COUNT)
    else:
        workers = min(16, CPU_COUNT)

    chunk_size = (n + workers - 1) // workers

    ranges = [
        (i * chunk_size, min((i + 1) * chunk_size, n))
        for i in range(workers)
        if i * chunk_size < n
    ]

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        chunks = list(executor.map(worker_sort, ranges))

    while len(chunks) > 1:
        next_chunks = []

        for i in range(0, len(chunks), 2):
            if i + 1 < len(chunks):
                next_chunks.append(merge(chunks[i], chunks[i + 1]))
            else:
                next_chunks.append(chunks[i])

        chunks = next_chunks

    return chunks[0]

def MAIN(input_file_path):
    global DATA_GLOBAL

    with open(input_file_path, 'r') as f:
        content = f.read().split()

    if not content:
        return []

    DATA_GLOBAL = []
    append = DATA_GLOBAL.append

    for i in range(1, len(content), 2):
        append((int(content[i]), content[i + 1]))

    n = len(DATA_GLOBAL)

    if n <= 1:
        return DATA_GLOBAL

    return parallel_merge_sort(n)

if __name__ == "__main__":
    import time

    start = time.perf_counter()
    result = MAIN("input.txt")
    print("Execution time:", time.perf_counter() - start)
    print(result)