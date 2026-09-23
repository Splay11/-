# 用栈做最近未匹配开启桩配对，统计内部长度能被 m 整除的舱段数


def count_cabin(n, m, t):
    # 栈里存尚未配对的 '(' 下标（从 0 起）
    st = []
    ans = 0
    for i in range(n):
        if t[i] == '(':
            # 开启桩入栈，等待之后最近的闭合桩来配对
            st.append(i)
        else:
            # 闭合桩与栈顶（左侧最近未匹配开启桩）配对
            left = st.pop()
            # 内部长度 = 两端下标差再减 1，即中间桩标个数
            inner = i - left - 1
            if inner % m == 0:
                ans += 1
    return ans


def main():
    n, m = map(int, input().split())
    t = input().strip()
    print(count_cabin(n, m, t))


if __name__ == "__main__":
    main()
