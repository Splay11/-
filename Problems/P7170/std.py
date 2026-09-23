def solve(x):
    """按位弹出个位接到答案后面。
    乘 10 之前判断会不会超出 32 位有符号整数范围，超了返回 0。
    负数按向 0 取整的除法和余数处理，和 C++ / Java 一致。
    """
    int_max = 2**31 - 1
    int_min = -(2**31)
    rev = 0
    while x != 0:
        if x >= 0:
            pop = x % 10
            x = x // 10
        else:
            # Python 的 // 和 % 是向下取整，这里改成向 0 取整
            pop = x % 10
            if pop > 0:
                pop -= 10
            x = -((-x) // 10)
        if rev > int_max // 10 or (rev == int_max // 10 and pop > 7):
            return 0
        if rev < int_min // 10 or (rev == int_min // 10 and pop < -8):
            return 0
        rev = rev * 10 + pop
    return rev


def main():
    # 一行一个 32 位有符号整数
    x = int(input())
    print(solve(x))


if __name__ == "__main__":
    main()
