import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    n = next(it)
    m = next(it)
    U = 500000

    freq = [0] * (U + 1)
    for _ in range(n):
        a = next(it)
        freq[a] += 1  # 统计每个分数出现次数

    divCnt = [0] * (U + 1)
    mulCnt = [0] * (U + 1)

    # 预处理 divCnt[x] = ∑_{d|x} freq[d]
    for d in range(1, U + 1):
        if freq[d] == 0:
            continue  # 小优化
        for x in range(d, U + 1, d):
            divCnt[x] += freq[d]

    # 预处理 mulCnt[x] = ∑_{k>=1} freq[k*x]
    for x in range(1, U + 1):
        s = 0
        for j in range(x, U + 1, x):
            s += freq[j]
        mulCnt[x] = s

    out_lines = []
    for _ in range(m):
        x = next(it)
        ans = divCnt[x] + mulCnt[x] - freq[x]
        out_lines.append(str(ans))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
