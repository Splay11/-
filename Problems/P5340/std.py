# 由序号构造前半段，镜像成回文后再转成十进制


def kth_palindrome(r, n, t):
    # 前半段长度：奇数时中间那一位也算在前半段里
    h = (n + 1) // 2
    half = [0] * h
    x = t - 1
    # 从右往左填前半段的低位，每一位都是 $0$ 到 $r-1$
    for i in range(h - 1, 0, -1):
        half[i] = x % r
        x //= r
    # 最高位不能为 $0$，所以在余下的数上再加 $1$
    half[0] = x + 1
    digits = [0] * n
    # 左右对称写下完整的 $n$ 位
    for i in range(h):
        digits[i] = half[i]
        digits[n - 1 - i] = half[i]
    val = 0
    # 按 $r$ 进制 Horner 法则转成十进制
    for d in digits:
        val = val * r + d
    return val


def main():
    r, n, t = map(int, input().split())
    print(kth_palindrome(r, n, t))


if __name__ == "__main__":
    main()
