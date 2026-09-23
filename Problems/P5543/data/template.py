import sys
import numpy as np

data = sys.stdin.read().strip().split()
it = iter(data)
C = int(next(it)); Hin = int(next(it)); Win = int(next(it))
inp = [[[0] * Win for _ in range(Hin)] for _ in range(C)]
for c in range(C):
    for h in range(Hin):
        for w in range(Win):
            inp[c][h][w] = int(next(it))
C2 = int(next(it)); Kh = int(next(it)); Kw = int(next(it))
kernel = [[[0] * Kw for _ in range(Kh)] for _ in range(C2)]
for c in range(C2):
    for h in range(Kh):
        for w in range(Kw):
            kernel[c][h][w] = int(next(it))
stride = int(next(it)); padding = int(next(it))
Y = Solution().multi_channel_conv(inp, kernel, stride, padding)
lines = [" ".join(str(int(v)) for v in row) for row in np.asarray(Y)]
sys.stdout.write("\n".join(lines) + "\n")
