def can_clear(s):
    # 每次核销都同时去掉一个 0 和一个 1
    # 只要两种字符都还在，串里一定存在相邻的 01 或 10
    # 所以能删空当且仅当 0 和 1 的个数相等
    return s.count("0") == s.count("1")


def count_clearable(strs):
    ans = 0
    for s in strs:
        if can_clear(s):
            ans += 1
    return ans


def main():
    m = int(input())
    strs = []
    for _ in range(m):
        strs.append(input().strip())
    print(count_clearable(strs))


if __name__ == "__main__":
    main()
