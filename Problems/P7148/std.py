def solve(s):
    """维护当前未匹配左括号数量的可能区间 [lo, hi]。
    左括号让区间整体加一，右括号整体减一，星号可以当左、当右或当空，
    所以 lo 减一、hi 加一。hi 一旦小于 0 说明右括号过多，不可能合法。
    lo 小于 0 时夹回 0，表示多出来的星号改当成空。
    扫完后 lo 必须为 0，才能把所有左括号配平。
    """
    lo = 0
    hi = 0
    for c in s:
        if c == "(":
            lo += 1
            hi += 1
        elif c == ")":
            lo -= 1
            hi -= 1
        else:
            # 星号：当右括号 / 空 / 左括号，区间向两边扩
            lo -= 1
            hi += 1
        if hi < 0:
            # 右括号已经多到星号也救不了
            return False
        if lo < 0:
            lo = 0
    return lo == 0


def main():
    # 一整行只有括号和星号
    s = input()
    print("true" if solve(s) else "false")


if __name__ == "__main__":
    main()
