def longest_keep(t, m):
    # 前缀里浅色 a、深色 b 各有多少颗，下标覆盖 0 到 m
    cnt_a = [0] * (m + 1)
    cnt_b = [0] * (m + 1)
    for i in range(m):
        cnt_a[i + 1] = cnt_a[i]
        cnt_b[i + 1] = cnt_b[i]
        if t[i] == "a":
            cnt_a[i + 1] += 1
        else:
            cnt_b[i + 1] += 1
    total_a = cnt_a[m]
    # best_diff：左端点不超过当前右端点时，左段 a 个数减去左段 b 个数的最大值
    best_diff = -10**18
    ans = 0
    for j in range(m + 1):
        diff = cnt_a[j] - cnt_b[j]
        if diff > best_diff:
            best_diff = diff
        # 右端点定在 j：左段用最优切分，中段把区间里的 b 全部留下，右段把后面的 a 全部留下
        cur = best_diff + cnt_b[j] + (total_a - cnt_a[j])
        if cur > ans:
            ans = cur
    return ans


def main():
    # 第一行是墨点数，第二行是条码
    m = int(input())
    t = input().strip()
    print(longest_keep(t, m))


if __name__ == "__main__":
    main()
