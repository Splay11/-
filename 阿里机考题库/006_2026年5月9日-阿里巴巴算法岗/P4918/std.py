import sys

def solve(L, g):
    # 前 cnt 个起点最终从左侧出界
    cnt = sum(1 for c in g if c == 'L')
    return 'L' * cnt + 'R' * (L - cnt)

q = int(input())
out = []
for _ in range(q):
    L = int(input())
    g = input().strip()
    out.append(solve(L, g))
sys.stdout.write('\n'.join(out))
