from collections import defaultdict

def main():
    # 输入数组大小 n 和查询次数 Q
    n, Q = map(int, input().split())
    
    # 输入数组
    a = list(map(int, input().split()))
    
    # 预处理：记录每个数的位置
    positions = defaultdict(list)
    for i in range(n):
        positions[a[i]].append(i + 1)  # 存储的是位置，位置从1开始
    
    # 处理每个查询
    for _ in range(Q):
        x, k = map(int, input().split())
        
        # 如果 x 在数组中出现的次数少于 k 次，返回 -1
        if len(positions[x]) < k:
            print(-1)
        else:
            # 返回 x 的第 k 次出现的位置
            print(positions[x][k - 1])

if __name__ == "__main__":
    main()
