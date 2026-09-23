import sys

def count_best(s, pL, pR, qL, qR):
    # 数位 DP：高位贪心取 1，同时满足区间 tight 限制
    dp = [0] * 16
    dp[15] = 1
    for pos in range(30, -1, -1):
        sb = (s >> pos) & 1
        plb, prb = (pL >> pos) & 1, (pR >> pos) & 1
        qlb, qrb = (qL >> pos) & 1, (qR >> pos) & 1
        nz, no = [0] * 16, [0] * 16
        has_one = False
        for st in range(16):
            cnt = dp[st]
            if not cnt:
                continue
            eq_pl, eq_pr = st & 1, (st >> 1) & 1
            eq_ql, eq_qr = (st >> 2) & 1, (st >> 3) & 1
            for pb in (0, 1):
                if eq_pl and pb < plb:
                    continue
                if eq_pr and pb > prb:
                    continue
                n_pl = 1 if eq_pl and pb == plb else 0
                n_pr = 1 if eq_pr and pb == prb else 0
                for qb in (0, 1):
                    if eq_ql and qb < qlb:
                        continue
                    if eq_qr and qb > qrb:
                        continue
                    n_ql = 1 if eq_ql and qb == qlb else 0
                    n_qr = 1 if eq_qr and qb == qrb else 0
                    ns = n_pl | (n_pr << 1) | (n_ql << 2) | (n_qr << 3)
                    cur = sb ^ pb ^ qb
                    if cur == 1:
                        no[ns] += cnt
                        has_one = True
                    else:
                        nz[ns] += cnt
        dp = no if has_one else nz
    return sum(dp)

data = list(map(int, sys.stdin.buffer.read().split()))
q, idx = data[0], 1
out = []
for _ in range(q):
    s = data[idx]
    pL, pR = data[idx + 1], data[idx + 2]
    qL, qR = data[idx + 3], data[idx + 4]
    idx += 5
    out.append(str(count_best(s, pL, pR, qL, qR)))
sys.stdout.write("\n".join(out))
