# 读取测试用例数量
t = int(input())
results = []

# 处理每个测试用例
for _ in range(t):
    # 读取每个测试用例的n和k
    n, k = map(int, input().split())

    # 读取数组a
    a = list(map(int, input().split()))

    # 初始化必要的变量
    MIN_VALUE = float('-inf')  
    dp = [MIN_VALUE] * (n + 2)
    pre = [MIN_VALUE] * (n + 2)
    udp = [MIN_VALUE] * (n + 2)
    suf = [MIN_VALUE] * (n + 2)

    # 计算最大子段和（前缀）
    for i in range(1, n + 1):
        dp[i] = max(a[i - 1], dp[i - 1] + a[i - 1])

    # 计算最大子段和的前缀最大值
    for i in range(1, n + 1):
        pre[i] = max(dp[i], pre[i - 1])

    # 计算最大字段和(后缀)
    for i in range(n, 0, -1):
        udp[i] = max(a[i - 1], udp[i + 1] + a[i - 1])

    # 计算最大字段和（后缀部分）
    for i in range(n, 0, -1):
        suf[i] = max(suf[i + 1], udp[i])

    # 计算最终结果
    res = MIN_VALUE
    for i in range(1, n - k + 1):
        res = max(res, pre[i] + suf[i + k + 1])

    results.append(res)

# 输出所有结果
print('\n'.join(map(str, results)))
