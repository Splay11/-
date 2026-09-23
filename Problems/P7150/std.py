def solve(s):
    """用栈消除相邻相同字母。
    当前字符和栈顶一样，就把这一对删掉；否则入栈。
    后面新来的字符还可能和新的栈顶再消，等价于反复删除直到不能再删。
    """
    stack = []
    for c in s:
        if stack and stack[-1] == c:
            # 相邻相同，成对删除
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)


def main():
    # 一整行小写字母
    s = input()
    print(solve(s))


if __name__ == "__main__":
    main()
