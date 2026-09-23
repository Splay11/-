def is_subsequence(a, b):
    i, j = 0, 0  # 初始化指针 i 和 j
    n, m = len(a), len(b)

    # 使用双指针判断子序列
    while i < n and j < m:
        if a[i] == b[j]:  # 如果匹配，移动 a 的指针
            i += 1
        j += 1  # 无论是否匹配，b 的指针都要移动

    # 判断是否匹配完所有元素
    if i == n:
        return "YES"
    else:
        return "NO"

# 主函数，读取输入
if __name__ == '__main__':
    n, m = map(int, input().split())  # 读取序列长度
    a = list(map(int, input().split()))  # 读取序列 a
    b = list(map(int, input().split()))  # 读取序列 b

    print(is_subsequence(a, b))
