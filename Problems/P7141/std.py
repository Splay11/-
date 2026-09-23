def solve(s):
    """对每个字母记下第一次和最后一次出现的下标。
    若某字母至少出现两次，中间长度为 last-first-1（不含两端）。
    所有字母都只出现一次则返回 -1；相邻两个相同字符中间长度是 0。
    """
    first = {}
    last = {}
    for i, c in enumerate(s):
        if c not in first:
            first[c] = i
        last[c] = i
    ans = -1
    for c in first:
        if last[c] > first[c]:
            # 只统计出现至少两次的字母
            length = last[c] - first[c] - 1
            if length > ans:
                ans = length
    return ans


def main():
    # 一整行就是字符串 s
    s = input()
    print(solve(s))


if __name__ == "__main__":
    main()
