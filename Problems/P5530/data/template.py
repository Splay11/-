import sys

data = sys.stdin.read().strip().split()
it = iter(data)
n = int(next(it))
k = int(next(it))
points = []
for _ in range(n):
    points.append([float(next(it)), float(next(it)), float(next(it))])
centers = Solution().kMeans(points, k)
for c in centers:
    print(f"{c[0]:.2f} {c[1]:.2f} {c[2]:.2f}")
