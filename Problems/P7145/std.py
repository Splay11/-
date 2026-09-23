def solve(s):
    """单调栈贪心：每个字母最终只留一次，且整体字典序最小。
    还没进栈的字母，若栈顶比它大、并且栈顶字母后面还会再出现，就可以弹出栈顶，
    把更小的字母尽量往前放。已经在栈里的字母直接跳过。
    """
    last = {}
    for i, c in enumerate(s):
        # 记下每个字母最后一次出现的下标，用来判断后面还能不能再用它
        last[c] = i
    stack = []
    used = set()
    for i, c in enumerate(s):
        if c in used:
            # 这个字母已经选过，相对顺序不能再插一次
            continue
        while stack and stack[-1] > c and last[stack[-1]] > i:
            # 栈顶更大，且后面还能再遇到它，弹掉以换更小的前缀
            used.remove(stack.pop())
        stack.append(c)
        used.add(c)
    return "".join(stack)


def main():
    # 一整行小写字母
    s = input()
    print(solve(s))


if __name__ == "__main__":
    main()
