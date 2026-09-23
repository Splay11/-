def is_integer(s):
    """整数：可选正负号，后面至少一位数字，且后面全是数字。"""
    if not s:
        return False
    i = 0
    if s[0] in "+-":
        i = 1
    if i >= len(s):
        return False
    return s[i:].isdigit()


def is_decimal(s):
    """小数：可选正负号，后面是 digits. / digits.digits / .digits 三种之一。"""
    if not s:
        return False
    i = 0
    if s[0] in "+-":
        i = 1
    rest = s[i:]
    if rest.count(".") != 1:
        return False
    left, right = rest.split(".")
    if left and not left.isdigit():
        return False
    if right and not right.isdigit():
        return False
    # 小数点两侧不能都没有数字，否则就是单独一个点
    return bool(left or right)


def valid(s):
    """有效数字 =（整数或小数）后面可以跟一个指数。
    指数是 e/E 加上一个整数。e/E 最多出现一次。
    """
    e_pos = -1
    for i, c in enumerate(s):
        if c == "e" or c == "E":
            if e_pos != -1:
                return False
            e_pos = i
    if e_pos == -1:
        return is_integer(s) or is_decimal(s)
    left = s[:e_pos]
    right = s[e_pos + 1 :]
    # 指数前后都不能空，右边必须是整数（可以带符号）
    if not left or not right:
        return False
    return (is_integer(left) or is_decimal(left)) and is_integer(right)


def solve(s):
    return "true" if valid(s) else "false"


def main():
    # 一整行就是待判断的字符串
    s = input()
    print(solve(s))


if __name__ == "__main__":
    main()
