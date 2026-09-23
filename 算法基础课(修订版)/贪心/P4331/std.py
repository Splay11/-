import sys
input = sys.stdin.readline

T = int(input())
for _ in range(T):
    n = int(input().strip())
    a = list(map(int, input().split()))
    c = list(map(int, input().split()))

    # 点赞值 -> 杂乱度列表
    mp = {}
    for ai, ci in zip(a, c):
        mp.setdefault(ai, []).append(ci)

    # 每个点赞值对应的杂乱度排序
    for k in mp:
        mp[k].sort()

    # 所有点赞值排序
    keys = sorted(mp.keys())
    ans = 0

    # 贪心组收藏夹
    while keys:
        while keys and keys[-1] not in mp:
            keys.pop()
        if not keys:
            break
        cur_max = 0
        # 从最大点赞值向左延续
        for i in range(len(keys) - 1, -1, -1):
            if i != len(keys) - 1 and keys[i] != keys[i + 1] - 1:
                break
            if keys[i] not in mp:
                break
            cur_max = max(cur_max, mp[keys[i]].pop())
            if not mp[keys[i]]:
                del mp[keys[i]]
        ans += cur_max
    print(ans)
