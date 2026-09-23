def feasible(vals, w, x):
    # 判定：是否存在长度至少为 w 的窗口，使得班均净值 >= x
    # 因为 x 是整数，floor(sum/len) >= x 等价于 sum (v_p - x) >= 0
    m = len(vals)
    pre = [0] * (m + 1)
    for i in range(m):
        pre[i + 1] = pre[i] + (vals[i] - x)
    # mn 维护 pre[0..r-w] 的最小值，对应窗口右端点 r、长度至少 w
    mn = 10**30
    for r in range(w, m + 1):
        if pre[r - w] < mn:
            mn = pre[r - w]
        if pre[r] - mn >= 0:
            return True
    return False


def max_floor_avg(vals, w):
    # 答案一定落在 [min v, max v]：单点不超过最大值，整段不低于最小值
    lo = min(vals)
    hi = max(vals)
    ans = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(vals, w, mid):
            # mid 可行，尝试更大的班均
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans


def main():
    g = int(input())
    answers = []
    for _ in range(g):
        m = int(input())
        w = int(input())
        # 第三行是逗号分隔的班次净值
        vals = list(map(int, input().split(",")))
        answers.append(str(max_floor_avg(vals, w)))
    print(" ".join(answers))


if __name__ == "__main__":
    main()
