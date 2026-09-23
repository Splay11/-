def min_range(v):
    # 枚举左右两半的分界，两半内部再各切一刀
    # 正数前缀和严格递增：半段内最优切点随边界右移只向右走
    n = len(v)
    s = [0] * (n + 1)
    for i in range(n):
        s[i + 1] = s[i] + v[i]
    total = s[n]
    ans = total
    i = 1
    k = 3
    # j 是第二段结尾下标（第 1..j 个为左半，至少 2 个，右边也至少 2 个）
    for j in range(2, n - 1):
        # 左半切点 i∈[1,j-1]，让两段和尽量接近 s[j]/2
        if i > j - 1:
            i = j - 1
        while i + 1 <= j - 1 and abs(2 * s[i + 1] - s[j]) <= abs(2 * s[i] - s[j]):
            i += 1
        # 右半切点 k∈[j+1,n-1]，让两段和尽量接近剩余一半
        if k <= j:
            k = j + 1
        while k + 1 <= n - 1 and abs(2 * (s[k + 1] - s[j]) - (total - s[j])) <= abs(2 * (s[k] - s[j]) - (total - s[j])):
            k += 1
        a = s[i]
        b = s[j] - s[i]
        c = s[k] - s[j]
        d = total - s[k]
        mx = max(a, b, c, d)
        mn = min(a, b, c, d)
        if mx - mn < ans:
            ans = mx - mn
    return ans


def main():
    m = int(input().strip())
    v = list(map(int, input().split()))
    print(min_range(v))


if __name__ == "__main__":
    main()
