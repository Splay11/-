def max_accept(n, b, v):
    # 第 i 人从当天驻场到第 n 天，共 (n-i) 天（下标从 0 计），每天耗 v[i]
    costs = []
    for i in range(n):
        costs.append(v[i] * (n - i))
    # 每人贡献都是 1，要人数最多就优先批准花费更小的
    costs.sort()
    used = 0
    ans = 0
    for c in costs:
        if used + c <= b:
            used += c
            ans += 1
        else:
            break
    return ans


def main():
    n, b = map(int, input().split())
    v = list(map(int, input().split()))
    print(max_accept(n, b, v))


if __name__ == "__main__":
    main()
