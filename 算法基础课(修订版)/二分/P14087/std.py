import bisect

def main():
    # 输入
    n, Q = map(int, input().split())  # n为数组大小，Q为查询次数
    arr = list(map(int, input().split()))  # 输入升序数组
    
    # 处理每个查询
    for _ in range(Q):
        target = int(input())  # 输入目标值
        
        # 查找比 target 小的最大值
        pos_max = bisect.bisect_left(arr, target) - 1
        max_val = arr[pos_max] if pos_max >= 0 else -1
        
        # 查找比 target 大的最小值
        pos_min = bisect.bisect_right(arr, target)
        min_val = arr[pos_min] if pos_min < n else -1
        
        # 输出结果
        print(max_val, min_val)

if __name__ == "__main__":
    main()
