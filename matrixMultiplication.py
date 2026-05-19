import multiprocessing
import time

def MAIN(input_file_path):
    with open(input_file_path, "r") as f:
        n = int(f.readline().strip())
        arr1 = []
        for _ in range(n):
            row = list(map(int, f.readline().split()))
            arr1.append(row)
        arr2 = []
        for _ in range(n):
            row = list(map(int, f.readline().split()))
            arr2.append(row)

    arr3 = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                arr3[i][j] += arr1[i][k] * arr2[k][j]
    return arr3

if __name__ == "__main__":
    start = time.perf_counter()
    print(MAIN("input.txt"))
    end = time.perf_counter()
    print("Thoi gian chay: ", end - start)
