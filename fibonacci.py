from multiprocessing import Pool
import time

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    n = int(input())

    start = time.time()

    with Pool(4) as p:
        results = p.map(fibonacci, range(n+1))
    
    end = time.time()
    print(results)
    print(f"Thời gian tính toán: {end - start:.4f} giây")

    
    start = time.time()

    resultss = fibonacci(n)
    
    end = time.time()

    print(resultss)
    print(f"Thời gian tính toán: {end - start:.4f} giây")
                

