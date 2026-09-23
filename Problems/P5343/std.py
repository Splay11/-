MOD = 1000000007


def path_sum(p):
    # S(p) = sum_{j=1}^{p} 2^{ctz(j)}
    # i ⊕ (i+1) = 2^{ctz(i+1)+1} - 1，故答案为 2*S(p) - p - 1
    s = 0
    k = 0
    while (1 << k) <= p:
        # ctz = k 的个数是 floor(p/2^k) - floor(p/2^{k+1})
        diff = (p >> k) - (p >> (k + 1))
        s += (1 << k) * diff
        k += 1
    return (2 * s - p - 1) % MOD


def solve_all(ps):
    return [path_sum(p) for p in ps]


def main():
    q = int(input())
    ps = []
    for _ in range(q):
        ps.append(int(input()))
    for ans in solve_all(ps):
        print(ans)


if __name__ == "__main__":
    main()
