def count_pairs(n, t, w):
    # 只关心重量对装载模数 t 的余数：w[i] + w[j] 是 t 的倍数
    # 当且仅当 (w[i]%t + w[j]%t) % t == 0
    cnt = [0] * t
    for x in w:
        cnt[x % t] += 1
    ans = 0
    # 余数 0 的货物只能和同类配对
    ans += cnt[0] * (cnt[0] - 1) // 2
    # t 为偶数时，余数 t/2 也只能和同类配对
    if t % 2 == 0:
        half = t // 2
        ans += cnt[half] * (cnt[half] - 1) // 2
    # 其余余数 r 只能和 t-r 配对，每对余数类只计一次
    for r in range(1, (t + 1) // 2):
        ans += cnt[r] * cnt[t - r]
    return ans


def main():
    # 第一行件数与装载模数，第二行各件重量
    n, t = map(int, input().split())
    w = list(map(int, input().split()))
    print(count_pairs(n, t, w))


if __name__ == "__main__":
    main()
