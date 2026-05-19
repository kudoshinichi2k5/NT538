import multiprocessing

# Sử dụng List thuần để tận dụng tính năng Arbitrary-precision (Số nguyên lớn vô hạn) của Python
global_A = None
global_B = None 
N = 0

def worker_multiply_ikj(bounds):
    global global_A, global_B, N
    start_row, end_row = bounds
    
    local_matrix = []
    local_sum = 0
    local_diag_main = []
    local_diag_sec = []
    
    for i in range(start_row, end_row):
        row_A = global_A[i]
        
        # Mảng kết quả cục bộ
        row_C = [0] * N
        
        # THUẬT TOÁN IKJ: Quét theo Hàng (Cache-Friendly)
        for k in range(N):
            val_A = row_A[k]
            
            # Tối ưu tự động cho ma trận thưa: Nếu A = 0, bỏ qua toàn bộ vòng lặp J
            if val_A == 0: 
                continue
                
            row_B = global_B[k]
            
            # Quét tuần tự liên tục trên List Python, CPU sẽ nạp trước dữ liệu vào L1 Cache
            for j in range(N):
                row_C[j] += val_A * row_B[j]
                
        local_matrix.append(row_C)
        
        # Thống kê ngay lập tức để giải phóng gánh nặng cho tiến trình Cha
        local_sum += sum(row_C)
        local_diag_main.append(row_C[i])
        local_diag_sec.append(row_C[N - 1 - i])
        
    return local_matrix, local_sum, local_diag_main, local_diag_sec

def MAIN(input_file_path):
    global global_A, global_B, N

    # Đọc trực tiếp và nạp vào biến toàn cục. 
    # List Comprehension ở tầng C giúp phân bổ bộ nhớ cực nhanh.
    with open(input_file_path, "r") as f:
        n = int(f.readline().strip())
        N = n
        
        global_A = [[int(x) for x in f.readline().split()] for _ in range(n)]
        global_B = [[int(x) for x in f.readline().split()] for _ in range(n)]

    num_cores = multiprocessing.cpu_count()
    chunk_size = (n + num_cores - 1) // num_cores
    
    # Gom bounds nhanh gọn
    bounds_list = [(i * chunk_size, min((i + 1) * chunk_size, n)) 
                   for i in range(num_cores) if i * chunk_size < n]

    # Server Linux sẽ fork 16 tiến trình, tái sử dụng hoàn toàn RAM của global_A và global_B
    with multiprocessing.Pool(processes=num_cores) as p:
        partial_results = p.map(worker_multiply_ikj, bounds_list)

    # Pha Reduce siêu nhẹ nhàng: 
    # Tiến trình Cha chỉ cần nối List mà không phải tính toán bất kỳ phép cộng nào nữa.
    C_matrix = []
    total_sum = 0
    diag_main = []
    diag_sec = []
    
    for mat_part, sum_part, main_part, sec_part in partial_results:
        C_matrix.extend(mat_part)
        total_sum += sum_part
        diag_main.extend(main_part)
        diag_sec.extend(sec_part)

    return {
        "matrix": C_matrix,
        "diag_main": diag_main,
        "diag_secondary": diag_sec,
        "total_sum": total_sum
    }

if __name__ == "__main__":
    import time
    start = time.perf_counter()
    res = MAIN("input.txt")
    end = time.perf_counter()
    print("Thời gian chạy với Ma Trận Thưa: ", end - start)