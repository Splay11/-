def solve(x):
    """负数带符号，从右往左读符号会跑到末尾，一定不是回文。
    不以 0 结尾（除了 0 本身）。翻转后半段数字，和前半段比较。
    不把整个整数转成字符串。
    """
    if x < 0:
        return False
    # 10、20 这类翻转后会有前导 0，不可能是回文
    if x != 0 and x % 10 == 0:
        return False
    rev = 0
    while x > rev:
        rev = rev * 10 + x % 10
        x //= 10
    # 偶数位：两半相等；奇数位：中间那一位可以丢掉
    return x == rev or x == rev // 10


def main():
    # 一行一个整数，范围是 32 位有符号整数
    x = int(input())
    print("true" if solve(x) else "false")


if __name__ == "__main__":
    main()
