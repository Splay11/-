import sys

data = sys.stdin.read().strip().split()
it = iter(data)
N = int(next(it))
K = int(next(it))
logits = []
for _ in range(N):
    logits.append([float(next(it)) for _ in range(K)])
labels = [int(next(it)) for _ in range(N)]
losses, avg, grads = Solution().crossEntropy(logits, labels)
print(" ".join(f"{x:.2f}" for x in losses))
print(f"{avg:.2f}")
for g in grads:
    print(" ".join(f"{x:.2f}" for x in g))
