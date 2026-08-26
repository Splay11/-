import math
v0, x, y = map(int, input().split())
if v0 == 0:
    t = math.sqrt(y / x)
else:
    s = math.sqrt(x * y)
    t = 0.0 if s <= v0 else (s - v0) / x
speed = v0 + t * x
print(f"{t + y / speed:.5f}")
