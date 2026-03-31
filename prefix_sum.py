from multiprocessing import Pool
import time

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def reduce(A, s, t):
    if s == t - 1:
        return TreeNode(A[s])
    mid = (s + t) // 2

    L = reduce(A, s, mid)
    R = reduce(A, mid, t)

    node = TreeNode(L.data + R.data)
    node.left = L
    node.right = R
    return node

def scan_r(root, B, s, t, offset):
    if s == t - 1:
        B[s] = root.data + offset
        return B
    mid = (s + t) // 2

    scan_r(root.left, B, s, mid, offset)
    scan_r(root.right, B, mid, t, offset + root.left.data)
    return B

def scan(A):
    n = len(A)
    piece = n // 4
     
    sub_arrays = [A[i*piece : (i+1)*piece] for i in range(4)]

    with Pool(4) as p:
        reduce_tasks = [
            p.apply_async(reduce, (sub_array, 0, len(sub_array)))
            for sub_array in sub_arrays
        ]

        roots = [task.get() for task in reduce_tasks]

        offsets = [0] * 4
        for i in range(1, 4):
            offsets[i] = offsets[i-1] + roots[i-1].data

        scan_tasks = []
        for i in range(4):
            empty_B = [0] * len(sub_arrays[i])

            task = p.apply_async(scan_r, (roots[i], empty_B, 0, len(empty_B), offsets[i]))
            scan_tasks.append(task)

        b = [task.get() for task in scan_tasks]

    return b[0] + b[1] + b[2] + b[3]

if __name__ == '__main__':
    A = list(range(1, 1001))
    B = scan(A)

    print(B)


