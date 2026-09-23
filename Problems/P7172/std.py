def solve(bits):
    """按题面公式：最高位是符号位，值为 -bits0 * 2^(n-1)，其余位按正权相加。
    n=1 时只有符号位，0 表示 0，1 表示 -1。
    """
    n = len(bits)
    ans = 0
    if bits[0] == 1:
        ans -= 1 << (n - 1)
    for i in range(1, n):
        if bits[i] == 1:
            ans += 1 << (n - 1 - i)
    return ans


def main():
    # 第一行 n，第二行 n 个 0/1，最高位在前
    n = int(input())
    bits = list(map(int, input().split()))
    print(solve(bits))


if __name__ == "__main__":
    main()
