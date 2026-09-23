def main():
    # 输入矩阵的行和列
    n, m = map(int, input().split())
    
    # 创建并输入矩阵
    matrix = []
    for i in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    
    # 输入查询次数
    q = int(input())
    
    while q > 0:
        q -= 1
        # 输入查询的坐标
        x1, y1, x2, y2 = map(int, input().split())
        
        # 转换为 0-indexed
        x1 -= 1
        y1 -= 1
        x2 -= 1
        y2 -= 1
        
        # 初始化最大值
        max_val = matrix[x1][y1]
        
        # 遍历子矩阵寻找最大值
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                max_val = max(max_val, matrix[i][j])
        
        # 输出结果
        print(max_val)

if __name__ == "__main__":
    main()
