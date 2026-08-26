import sys
data = list(map(int, sys.stdin.read().split()))
n, a = data[0], data[1:]
best = cur = 1
for i in range(1, n):
    if abs(a[i] - a[i - 1]) <= 1:
        cur += 1
    else:
        cur = 1
    best = max(best, cur)
print(best)
