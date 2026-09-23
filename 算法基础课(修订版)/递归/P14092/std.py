def uniquePaths(x, y, n):
    # 基本情况：如果到达右下角 (n-1, n-1)，返回 1
    if x == n - 1 and y == n - 1:
        return 1

    paths = 0

    # 向下走
    if x < n - 1:
        paths += uniquePaths(x + 1, y, n)  # 递归计算向下走的路径数

    # 向右走
    if y < n - 1:
        paths += uniquePaths(x, y + 1, n)  # 递归计算向右走的路径数

    return paths

# 主函数
if __name__ == "__main__":
    n = int(input())  # 输入网格的大小
    print(uniquePaths(0, 0, n))  # 从 (0, 0) 出发
