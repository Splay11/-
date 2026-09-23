import sys

data = sys.stdin.read().strip().split()
it = iter(data)
n = int(next(it)); eps = float(next(it))
adv, lp, olp = [], [], []
for _ in range(n):
    adv.append(float(next(it)))
    lp.append(float(next(it)))
    olp.append(float(next(it)))
print(f"{Solution().ppoClippedLoss(adv, lp, olp, eps):.4f}")
