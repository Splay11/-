import sys
# 递归深度设置为1000000
sys.setrecursionlimit(1000000)

n_and_rest = sys.stdin.read().split()
n = int(n_and_rest[0])
h = list(map(int, n_and_rest[1:n+1]))
h = [0] + h  # 1-based indexing

def min_cost(l, r):
    if l > r:
        # 空区间的操作代价为0
        return 0
    if l == r:
        # 一个服务器的操作默认为单列操作
        return 2 
    min_h = min(h[l:r+1])
    # 操作1: 用行操作，找到<不是最小高度>的连续区间
    cost1 = 1
    i = l
    while i <= r:
        # 找到连续区间
        if h[i] > min_h:
            # 找到连续区间的起始位置
            start = i
            # 找到连续区间的终止位置
            while i <= r and h[i] > min_h:
                i += 1
            # 递归计算连续区间的最小代价
            cost1 += min_cost(start, i - 1)
        else:
            i += 1
    return cost1

total_min_cost = min_cost(1, n)
print(total_min_cost)
