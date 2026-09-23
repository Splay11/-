def is_valid(t):
    # 栈里只放还没配上的开封口；遇闭封口必须立刻配栈顶
    pair = {")": "(", "]": "[", "}": "{"}
    st = []
    for ch in t:
        if ch in "([{":
            # 开封口：记下，等后面的闭封口来配
            st.append(ch)
        else:
            # 闭封口：栈空或种类对不上，就是交叉或多余
            if (not st) or st[-1] != pair[ch]:
                return False
            st.pop()
    # 栈里还有开封口，说明有没扣上的
    return not st


def main():
    # 一行记录；空文件按空串处理
    try:
        t = input()
    except EOFError:
        t = ""
    if is_valid(t):
        print("true")
    else:
        print("false")


if __name__ == "__main__":
    main()
