from collections import Counter

q = int(input())
for _ in range(q):
    m = int(input())
    x = list(map(int, input().split()))
    y = list(map(int, input().split()))
    p = list(map(int, input().split()))  # 1 下标指向 y
    freq = Counter()
    ans = 0
    for v in range(m):
        freq[x[v]] += 1  # 先纳入前缀 x_1..x_v
        ans += freq[y[p[v] - 1]]  # 统计等于 y_{p_v} 的个数
    print(ans)
