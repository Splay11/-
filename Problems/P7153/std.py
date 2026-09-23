def solve(s):
    """dp[i] 表示前 i 个字符有多少种解码方法。
    一位：当前数字不是 0，才能接在前 i-1 的方案后面。
    两位：最后两位数在 10 到 26 之间（自然排除前导零），才能接在前 i-2 的方案后面。
    """
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        # 单独解码 s[i-1]
        if s[i - 1] != "0":
            dp[i] += dp[i - 1]
        if i >= 2:
            # 把 s[i-2..i-1] 当成一个字母，必须是 10..26
            x = (ord(s[i - 2]) - 48) * 10 + (ord(s[i - 1]) - 48)
            if 10 <= x <= 26:
                dp[i] += dp[i - 2]
    return dp[n]


def main():
    # 一整行数字串，可能含前导零
    s = input()
    print(solve(s))


if __name__ == "__main__":
    main()
