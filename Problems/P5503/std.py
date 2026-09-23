def kth_largest(matrix, k):
    # 展平后排序取第 K 大；总元素不超过 500*500
    vals = []
    for row in matrix:
        vals.extend(row)
    vals.sort(reverse=True)
    return vals[k - 1]


def main():
    n, m, k = map(int, input().split())
    matrix = []
    for _ in range(n):
        matrix.append(list(map(int, input().split())))
    print(kth_largest(matrix, k))


if __name__ == "__main__":
    main()
