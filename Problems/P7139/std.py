def solve(s):
    """枚举每个中心，向两边扩张，统计回文子串个数。
    奇数长度中心是一个字符，偶数长度中心在两个字符之间。
    相同内容但位置不同的子串要分别计数。
    """
    n = len(s)
    ans = 0

    def expand(left, right):
        # 只要左右字符相等，就找到一个回文，继续往外扩
        cnt = 0
        while left >= 0 and right < n and s[left] == s[right]:
            cnt += 1
            left -= 1
            right += 1
        return cnt

    for i in range(n):
        # 以 s[i] 为中心的奇数回文
        ans += expand(i, i)
        # 以 s[i] 和 s[i+1] 缝为中心的偶数回文
        ans += expand(i, i + 1)
    return ans


def main():
    # 一整行就是字符串 s，没有空格
    s = input()
    print(solve(s))


if __name__ == "__main__":
    main()
