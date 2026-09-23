# 恰好选 4 件、总价不超过 10000：先用位集求最大总价，再按编号从小到大贪心。

CAP = 10000
NEED = 4


def pick_four(b, w):
    n = len(b)
    if n < NEED:
        return None
    order = sorted(range(n), key=lambda i: b[i])
    b = [b[i] for i in order]
    w = [w[i] for i in order]
    mask = (1 << (CAP + 1)) - 1
    # suffix[i][k]：从下标 i 到末尾恰好选 k 件，能凑出的总价集合（位集）
    cur = [0] * (NEED + 1)
    cur[0] = 1
    suffix = [None] * (n + 1)
    suffix[n] = cur[:]
    for i in range(n - 1, -1, -1):
        nxt = cur[:]
        ww = w[i]
        for k in range(NEED - 1, -1, -1):
            # dp[i][k][s]：从 i 往后恰好选 k 件，总价能否为 s
            # 不选第 i 件：nxt 已拷贝 cur，即继承 dp[i+1][k]
            # 选第 i 件：左移 w[i] 位等于总价整体加上售价，或进 dp[i][k+1]
            # k 从大到小，保证每件最多用一次；掩码丢掉超过 10000 的总价
            nxt[k + 1] = (nxt[k + 1] | (cur[k] << ww)) & mask
        cur = nxt
        suffix[i] = cur[:]
    bits = suffix[0][NEED]
    if bits == 0:
        return None
    # 不超过上限的最大可达总价
    remain_s = bits.bit_length() - 1
    remain_k = NEED
    ans = []
    for i in range(n):
        if remain_k == 0:
            break
        ns = remain_s - w[i]
        nk = remain_k - 1
        # 判断 dp[i+1][nk][ns] 是否为真：选完当前件后后缀还能不能凑齐
        # 编号已从小到大排好，能选就选，得到字典序最小的一组
        if ns >= 0 and ((suffix[i + 1][nk] >> ns) & 1):
            ans.append(b[i])
            remain_s = ns
            remain_k = nk
    return ans


def main():
    m = int(input())
    b = []
    w = []
    for _ in range(m):
        bi, wi = map(int, input().split())
        b.append(bi)
        w.append(wi)
    ans = pick_four(b, w)
    if ans is None:
        print(0)
    else:
        print(" ".join(str(x) for x in ans))


if __name__ == "__main__":
    main()
