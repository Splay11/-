# 滑动窗口：对每个右端点，无重复窗口 [left, right] 内长度为 k 及以上的子串个数可 O(1) 计算


def count_unique(s, k):
    n = len(s)
    # last[c]：字符 c 上一次出现的下标，-1 表示还没出现过
    last = [-1] * 26
    left = 0
    ans = 0
    for right in range(n):
        idx = ord(s[right]) - 97
        # 窗口内出现重复，把左端推到上一次该字符的右边
        if last[idx] >= left:
            left = last[idx] + 1
        last[idx] = right
        # 以 right 为右端、长度 >= k 的起点最多到 right-k+1，且不能小于 left
        limit = right - k + 1
        if limit >= left:
            ans += limit - left + 1
    return ans


def main():
    s = input().strip()
    k = int(input())
    print(count_unique(s, k))


if __name__ == "__main__":
    main()
