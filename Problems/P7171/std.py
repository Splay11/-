def gcd(a, b):
    """辗转相除求最大公约数。"""
    while b:
        a, b = b, a % b
    return a


def solve(n):
    """从 1 累乘到 n，每步用 lcm(ans, i) = ans / gcd(ans, i) * i。
    先除后乘避免中间结果不必要地变大。
    """
    ans = 1
    for i in range(1, n + 1):
        g = gcd(ans, i)
        ans = ans // g * i
    return ans


def main():
    # 一行正整数 n，1 到 40
    n = int(input())
    print(solve(n))


if __name__ == "__main__":
    main()
