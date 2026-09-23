import sys
from bisect import bisect_left

def count_pairs(pulse, gauge, bound):
    """统计交叉表 pulse[i] * gauge[j] >= bound 的格子数"""
    gauge = sorted(gauge)
    C = len(gauge)
    ans = 0
    for p in pulse:
        if bound == 0:
            ans += C
        elif p == 0:
            continue
        else:
            need = (bound + p - 1) // p
            pos = bisect_left(gauge, need)
            ans += C - pos
    return ans

data = list(map(int, sys.stdin.buffer.read().split()))
idx = 0
T = data[idx]
idx += 1
res = []

for _ in range(T):
    R = data[idx]
    C = data[idx + 1]
    bound = data[idx + 2]
    idx += 3
    pulse = data[idx:idx + R]
    idx += R
    gauge = data[idx:idx + C]
    idx += C
    res.append(str(count_pairs(pulse, gauge, bound)))

print("\n".join(res))
