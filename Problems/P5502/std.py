def find_elements(a):
    n = len(a)
    # pref_max[i] = a[0..i] 的最大值
    pref_max = [0] * n
    pref_max[0] = a[0]
    for i in range(1, n):
        pref_max[i] = a[i] if a[i] > pref_max[i - 1] else pref_max[i - 1]
    # suf_min[i] = a[i..n-1] 的最小值
    suf_min = [0] * n
    suf_min[n - 1] = a[n - 1]
    for i in range(n - 2, -1, -1):
        suf_min[i] = a[i] if a[i] < suf_min[i + 1] else suf_min[i + 1]
    ans = []
    for i in range(n):
        # 比左边都大：i==0 或 a[i] > pref_max[i-1]
        # 比右边都小：i==n-1 或 a[i] < suf_min[i+1]
        left_ok = (i == 0) or (a[i] > pref_max[i - 1])
        right_ok = (i == n - 1) or (a[i] < suf_min[i + 1])
        if left_ok and right_ok:
            ans.append(a[i])
    return ans


def main():
    n = int(input().strip())
    a = list(map(int, input().split()))
    ans = find_elements(a)
    if ans:
        print(" ".join(str(x) for x in ans))
    else:
        print()


if __name__ == "__main__":
    main()
