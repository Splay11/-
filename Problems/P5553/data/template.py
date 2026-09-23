import sys

data = sys.stdin.read().strip().split()
it = iter(data)
L = int(next(it)); V = int(next(it))
tokens = [int(next(it)) for _ in range(L)]
logits = [[float(next(it)) for _ in range(V)] for _ in range(L)]
print(f"{Solution().sftCrossEntropy(tokens, logits):.4f}")
