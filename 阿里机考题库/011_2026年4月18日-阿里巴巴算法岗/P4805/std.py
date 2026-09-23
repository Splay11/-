import sys


def solve_case(m, vals):
    # 按优先级分值从高到低排序
    vals.sort(reverse=True)

    team_a = 0  # 甲组累计分值
    team_b = 0  # 乙组累计分值

    # 排序后双方轮流取：偶数下标归甲组，奇数下标归乙组
    for i in range(m):
        if i % 2 == 0:
            team_a += vals[i]
        else:
            team_b += vals[i]

    return team_a - team_b


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    ans = []

    for _ in range(t):
        m = data[idx]
        idx += 1
        vals = data[idx:idx + m]
        idx += m
        ans.append(str(solve_case(m, vals)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()
