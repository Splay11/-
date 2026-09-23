def process(s):
    # 先去掉所有 b
    buf = []
    for ch in s:
        if ch != 'b':
            buf.append(ch)
    # 再用栈消除连续的 ac（可反复相邻形成）
    st = []
    for ch in buf:
        if st and st[-1] == 'a' and ch == 'c':
            st.pop()
        else:
            st.append(ch)
    return "".join(st)


def main():
    s = input().strip()
    print(process(s))


if __name__ == "__main__":
    main()
