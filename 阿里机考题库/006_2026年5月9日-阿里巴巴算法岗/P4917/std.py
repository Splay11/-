import sys

def build(m):
    # m mod 4 为 1 或 2 时 1..m 总和为奇数，无解
    if m % 4 in (1, 2):
        return None
    w = []
    if m % 4 == 3:
        w.extend([1, 2, -3])
        start = 4
    else:
        start = 1
    for x in range(start, m + 1, 4):
        w.extend([x, -(x + 1), -(x + 2), x + 3])
    return w

q = int(input())
out = []
for _ in range(q):
    m = int(input())
    w = build(m)
    out.append("-1" if w is None else " ".join(map(str, w)))
sys.stdout.write("\n".join(out))
