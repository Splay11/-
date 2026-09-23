def solve(s):
    """用栈处理括号，线性扫一遍表达式。
    res 是当前这一层已经算完的值，sign 是下一个数字或括号前的正负号。
    遇到左括号就把当前层的 res 和 sign 压栈，里面重新从 0 算；
    遇到右括号就把内层结果乘上括号前的符号，加回外层。
    """
    stack = []
    res = 0
    sign = 1
    n = len(s)
    i = 0
    while i < n:
        c = s[i]
        if c == " ":
            # 空格没有意义，直接跳过
            i += 1
            continue
        if c.isdigit():
            # 把连续数字拼成一个整数
            num = 0
            while i < n and s[i].isdigit():
                num = num * 10 + ord(s[i]) - 48
                i += 1
            res += sign * num
            continue
        if c == "+":
            # 加号只能当二元运算符，下一个项取正
            sign = 1
            i += 1
            continue
        if c == "-":
            # 减号既可二元也可一元，效果都是下一个项取负
            sign = -1
            i += 1
            continue
        if c == "(":
            # 进入新括号层：外层结果和括号前符号先存起来
            stack.append(res)
            stack.append(sign)
            res = 0
            sign = 1
            i += 1
            continue
        # 右括号：用括号前符号把内层结果并回外层
        prev_sign = stack.pop()
        prev_res = stack.pop()
        res = prev_res + prev_sign * res
        i += 1
    return res


def main():
    # 表达式可能含空格，必须整行读入
    s = input()
    print(solve(s))


if __name__ == "__main__":
    main()
