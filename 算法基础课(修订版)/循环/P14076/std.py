def main():
    # 读取输入
    n = int(input())
    arr = list(map(int, input().split()))
    
    q = int(input())
    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1  # 转换为0开始的索引
        r -= 1
        
        max_value = arr[l]
        max_indices = [l + 1]  # 初始化下标列表（1开始）
        
        for i in range(l + 1, r + 1):
            if arr[i] > max_value:
                max_value = arr[i]
                max_indices = [i + 1]
            elif arr[i] == max_value:
                max_indices.append(i + 1)
        
        # 输出结果
        print(max_value)
        print(' '.join(map(str, max_indices)))

if __name__ == "__main__":
    main()
