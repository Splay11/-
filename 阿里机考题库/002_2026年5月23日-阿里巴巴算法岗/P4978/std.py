q = int(input())
for _ in range(q):
    m, s = map(int, input().split())
    h = list(map(int, input().split()))
    # 硬度从大到小：优先尝试更硬的工件
    h.sort(reverse=True)
    cnt = 0
    for x in h:
        # 已成功 cnt 次，当前耐久为 s - cnt
        if s - cnt >= x:
            cnt += 1
    print(cnt)
