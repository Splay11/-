def solve(s):
    """用栈解码嵌套的 k[串]。
    遇到数字就累加成 k，遇到 [ 就把当前已经拼好的串和 k 压栈，
    括号里面重新开始拼；遇到 ] 弹出 k 和外面的串，把里面的结果重复 k 次接回去。
    普通字母直接接到当前串后面。
    """
    stack = []
    cur = []
    num = 0
    for c in s:
        if c.isdigit():
            # k 可能有多位，例如 300
            num = num * 10 + ord(c) - 48
        elif c == "[":
            # 进入新一层括号，外层结果先存起来
            stack.append(("".join(cur), num))
            cur = []
            num = 0
        elif c == "]":
            prev, k = stack.pop()
            # 内层解码结果重复 k 次，再接到外层后面
            cur = list(prev + "".join(cur) * k)
        else:
            cur.append(c)
    return "".join(cur)


def main():
    # 一整行编码串，不含空格
    s = input()
    print(solve(s))


if __name__ == "__main__":
    main()
