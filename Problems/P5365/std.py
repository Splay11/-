import bisect


def max_boats(a, b):
    # 起点小的那条若终点不更小，就会追上或堵在终点，因此会相撞
    # 按起点升序、终点降序排序后，对终点求最长严格上升子序列
    pairs = []
    for i in range(len(a)):
        pairs.append((a[i], b[i]))
    pairs.sort(key=lambda x: (x[0], -x[1]))
    tails = []
    for _, dest in pairs:
        pos = bisect.bisect_left(tails, dest)
        if pos == len(tails):
            tails.append(dest)
        else:
            tails[pos] = dest
    return len(tails)


def main():
    q = int(input().strip())
    for _ in range(q):
        m = int(input().strip())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        print(max_boats(a, b))


if __name__ == "__main__":
    main()
