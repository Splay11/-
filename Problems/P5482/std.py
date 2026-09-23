import heapq
from collections import defaultdict


def max_score(types, values, k):
    # 按类型分组，组内价值从大到小，再按每种最大价值排序
    groups = defaultdict(list)
    for t, v in zip(types, values):
        groups[t].append(v)
    arr = []
    for vs in groups.values():
        vs.sort(reverse=True)
        arr.append(vs)
    arr.sort(key=lambda vs: -vs[0])

    ans = 0
    found = False
    extras = []
    used = []
    sum_used = 0
    head = 0
    total = 0
    for d, vs in enumerate(arr, 1):
        # 选中这一种：必须拿它最贵的一朵，剩下的进备用堆
        head += vs[0]
        total += len(vs)
        for x in vs[1:]:
            heapq.heappush(extras, -x)
        r = k - d
        if r < 0:
            break
        # used 里只保留当前还需要的 r 朵「同种续选」
        while used and len(used) > r:
            x = heapq.heappop(used)
            sum_used -= x
            heapq.heappush(extras, -x)
        while extras and len(used) < r:
            x = -heapq.heappop(extras)
            heapq.heappush(used, x)
            sum_used += x
        while extras and used and -extras[0] > used[0]:
            bad = heapq.heappop(used)
            sum_used -= bad
            good = -heapq.heappop(extras)
            heapq.heappush(used, good)
            sum_used += good
            heapq.heappush(extras, -bad)
        # 已选种类凑得出 k 朵时，更新答案：价值和 + 种类平方
        if total >= k and len(used) == r:
            cur = head + sum_used + d * d
            if (not found) or cur > ans:
                ans = cur
                found = True
    return ans


def main():
    # 第一行 n、k，随后两行分别是类型和价值
    parts = list(map(int, input().split()))
    n = parts[0]
    k = parts[1]
    types = list(map(int, input().split()))
    values = list(map(int, input().split()))
    print(max_score(types[:n], values[:n], k))


if __name__ == "__main__":
    main()
