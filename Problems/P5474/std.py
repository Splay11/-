import bisect


def min_ops(values, targets):
    # 排序后用前缀和，每次任务 O(log m) 算 sum |v-g|
    arr = sorted(values)
    m = len(arr)
    pref = [0] * (m + 1)
    for i in range(m):
        pref[i + 1] = pref[i] + arr[i]
    # 奇偶个数固定，用来把 sum |v-g| 改成 sum floor(|v-g|/2)
    odd = 0
    for x in values:
        if x & 1:
            odd += 1
    even = m - odd
    ans = []
    for g in targets:
        # 小于 g、大于 g 的两段分别贡献绝对值
        lt = bisect.bisect_left(arr, g)
        gt = bisect.bisect_right(arr, g)
        sum_lt = pref[lt]
        sum_gt = pref[m] - pref[gt]
        cnt_gt = m - gt
        sabs = g * lt - sum_lt + sum_gt - g * cnt_gt
        # 与 g 不同奇偶的数，floor 会各丢掉 1
        diff = even if (g & 1) else odd
        ans.append((sabs - diff) // 2)
    return ans


def main():
    # 先读节点台数和偏移，再读任务条数与每个目标档
    m = int(input())
    values = list(map(int, input().split()))
    k = int(input())
    targets = []
    for _ in range(k):
        targets.append(int(input()))
    ans = min_ops(values[:m], targets)
    # 每项任务单独一行
    for x in ans:
        print(x)


if __name__ == "__main__":
    main()
