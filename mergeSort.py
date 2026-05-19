C = None

def mergeSort(B, A, n):
    global C
    if n == 1:
        B[0] = A[0]
        return B
    mid = n // 2
    C = [0] * n
    mergeSort(C, A, mid)
    mergeSort(C[mid:], A[mid:], n - mid)
    merge(C, n/2, C[mid:], n - n/2)

def merge(A, na, B, nb):
    p1 = 0
    p2 = 0
    while p1 < na and p2 < nb:
        if A[p1] < B[p2]:
            C.append(A[p1])
            p1 += 1
        else:
            C.append(B[p2])
            p2 += 1
    while p1 < na:
        C.append(A[p1])
        p1 += 1
    while p2 < nb:
        C.append(B[p2])
        p2 += 1
    

if __name__ == "__main__":
    arr = [38, 27, 43, 3, 9, 82, 10]
    ans = None
    print("Given array is", arr)
    ans = mergeSort(ans, arr, len(arr))
    print("Sorted array is: ", ans)