MOD = 10**9 + 7


def segment_contribution(length):
    # 长度为 length 的合规差分段贡献 length*(length-1)*(length+1)/6
    return length * (length - 1) * (length + 1) // 6


def count_turn_points(m, readings):
    if m < 3:
        return 0

    total = 0
    run_len = 1  # 当前合规差分段长度

    for i in range(1, m - 1):
        delta_left = readings[i] - readings[i - 1]
        delta_right = readings[i + 1] - readings[i]
        # 相邻差分异号或含零，说明该内部测点是拐点
        if delta_left * delta_right <= 0:
            run_len += 1
        else:
            total = (total + segment_contribution(run_len)) % MOD
            run_len = 1

    total = (total + segment_contribution(run_len)) % MOD
    return total


def main():
    t = int(input())
    out_lines = []
    for _ in range(t):
        m = int(input())
        readings = list(map(int, input().split()))
        out_lines.append(str(count_turn_points(m, readings)))
    print("\n".join(out_lines))


if __name__ == "__main__":
    main()
