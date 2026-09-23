def max_pairs(d, v):
    # (x+d)*(y+d) 为偶数 <=> 至少一个数与 d 同奇偶
    # 与 d 同奇偶的放 same，不同的放 diff；diff 只能和 same 配
    same = []
    diff = []
    for x in v:
        if x % 2 == d % 2:
            same.append(x)
        else:
            diff.append(x)
    pairs = []
    i = 0
    j = 0
    # 先把不同奇偶的配给 same
    while i < len(diff) and j < len(same):
        pairs.append((diff[i], same[j]))
        i += 1
        j += 1
    # 剩下的 same 两两配对
    while j + 1 < len(same):
        pairs.append((same[j], same[j + 1]))
        j += 2
    return pairs


def main():
    parts = input().split()
    m = int(parts[0])
    d = int(parts[1])
    v = list(map(int, input().split()))
    pairs = max_pairs(d, v)
    print(len(pairs))
    for x, y in pairs:
        print(x, y)


if __name__ == "__main__":
    main()
