import numpy as np


class Solution:
    def multi_channel_conv(self, inp, kernel, stride, padding):
        # 单个多通道核，无 bias、无 Cout：输出为 H_out x W_out
        x = np.asarray(inp, dtype=np.int64)  # (C,H,W)
        k = np.asarray(kernel, dtype=np.int64)  # (C,Kh,Kw)
        C, H, W = x.shape
        _, Kh, Kw = k.shape
        # padding
        if padding > 0:
            x = np.pad(x, ((0, 0), (padding, padding), (padding, padding)), mode="constant")
        _, Hp, Wp = x.shape
        Hout = (Hp - Kh) // stride + 1
        Wout = (Wp - Kw) // stride + 1
        out = np.zeros((Hout, Wout), dtype=np.int64)
        for i in range(Hout):
            for j in range(Wout):
                # 窗口与核逐通道点积再求和
                window = x[:, i * stride : i * stride + Kh, j * stride : j * stride + Kw]
                out[i, j] = np.sum(window * k)
        return out


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    C = int(next(it)); Hin = int(next(it)); Win = int(next(it))
    inp = [[[0] * Win for _ in range(Hin)] for _ in range(C)]
    for c in range(C):
        for h in range(Hin):
            for w in range(Win):
                inp[c][h][w] = int(next(it))
    C2 = int(next(it)); Kh = int(next(it)); Kw = int(next(it))
    assert C2 == C
    kernel = [[[0] * Kw for _ in range(Kh)] for _ in range(C)]
    for c in range(C):
        for h in range(Kh):
            for w in range(Kw):
                kernel[c][h][w] = int(next(it))
    stride = int(next(it)); padding = int(next(it))
    Y = Solution().multi_channel_conv(inp, kernel, stride, padding)
    lines = [" ".join(str(int(v)) for v in row) for row in Y]
    sys.stdout.write("\n".join(lines) + "\n")
