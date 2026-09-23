# 用可用数字拼出严格小于 s 的最大整数（按字符串处理大整数）

def max_of_len(L, digits):
    """构造长度为 L 的最大合法数（无前导零）；不可能则返回 None"""
    digits = sorted(digits)
    nz = [d for d in digits if d > 0]
    if L <= 0:
        return None
    if not nz:
        # 只有 0：仅单位数 0
        return "0" if L == 1 and 0 in digits else None
    mx = digits[-1]
    return str(nz[-1]) + str(mx) * (L - 1)


def max_same_len_lt(s, digits):
    """构造与 s 等长且严格小于 s 的最大数；无前导零（迭代，避免长串爆栈）"""
    digits = set(digits)
    mx = max(digits)
    n = len(s)
    sdig = [int(c) for c in s]

    # 从右往左找第一个可减小的位置，使前缀尽量长从而数值最大
    for i in range(n - 1, -1, -1):
        ok = True
        for j in range(i):
            if sdig[j] not in digits:
                ok = False
                break
            # 等长多位数禁止前导零
            if j == 0 and n > 1 and sdig[j] == 0:
                ok = False
                break
        if not ok:
            continue
        # 在第 i 位放严格小于 s[i] 的最大可用数字
        cands = [d for d in digits if d < sdig[i]]
        if i == 0 and n > 1:
            cands = [d for d in cands if d != 0]
        if not cands:
            continue
        d = max(cands)
        res = sdig[:i] + [d] + [mx] * (n - i - 1)
        return "".join(map(str, res))
    return None


def better(a, b):
    """比较两个无前导零的数字串，返回较大者"""
    if a is None:
        return b
    if b is None:
        return a
    if len(a) != len(b):
        return a if len(a) > len(b) else b
    return a if a >= b else b


def main():
    n = int(input())
    nums = list(map(int, input().split()))
    s = input().strip()  # 可能很长，按字符串读
    digits = set(nums)

    best = max_same_len_lt(s, digits)

    # 更短的数一定更小；取最长更短长度即为 len(s)-1
    if len(s) > 1:
        shorter = max_of_len(len(s) - 1, digits)
        best = better(best, shorter)

    if best is None:
        print(-1)
    else:
        print(best)


if __name__ == "__main__":
    main()
