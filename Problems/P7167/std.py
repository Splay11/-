def solve(answers):
    """回答 x 表示该颜色一共有 x+1 只。
    统计每种回答出现几次，能塞进同一颜色组就尽量塞，不够再开新组。
    最少兔子数 = 组数 * 每组容量。
    """
    cnt = {}
    for x in answers:
        cnt[x] = cnt.get(x, 0) + 1
    ans = 0
    for x, c in cnt.items():
        size = x + 1
        # 向上取整：c 只回答 x 的兔子需要多少个容量为 size 的颜色组
        groups = (c + size - 1) // size
        ans += groups * size
    return ans


def main():
    # 第一行 n，第二行 n 个回答
    n = int(input())
    answers = list(map(int, input().split()))
    print(solve(answers))


if __name__ == "__main__":
    main()
