MOD = 10**9 + 7
q = int(input())
for _ in range(q):
    m = int(input())
    h = list(map(int, input().split()))
    st = []  # (最小值, 段数)
    cur = 0  # 当前 G(k)
    ans = 0
    for k, x in enumerate(h, 1):
        cnt = 1
        while st and st[-1][0] >= x:
            v, c = st.pop()
            cur -= v * c  # 旧最小值失效
            cnt += c
        st.append((x, cnt))
        cur += x * cnt
        cur %= MOD
        ans = (ans + cur * (m - k + 1)) % MOD
    print(ans)
