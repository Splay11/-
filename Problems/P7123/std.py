def longest_common_subarray(a, b):
    """求两个数组最长公共子数组（必须连续）的长度。"""
    n = len(a)
    m = len(b)
    # dp[i][j]：以 a[i-1]、b[j-1] 结尾的公共子数组最长能有多长
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    ans = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                # 当前这一对相等，长度就是左上角那格再加 1
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > ans:
                    ans = dp[i][j]
            # 不相等时 dp[i][j] 保持 0：公共子数组在这里断开
    return ans


def main():
    # 第一行：两个数组的长度
    n, m = map(int, input().split())
    # 第二行、第三行：nums1、nums2
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    print(longest_common_subarray(a, b))


if __name__ == "__main__":
    main()
