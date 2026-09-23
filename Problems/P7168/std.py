def solve(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    """两个轴对齐矩形面积之和减去重叠。
    重叠宽高取两段区间的交集长度，没有交集就是 0。
    """
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    w = min(ax2, bx2) - max(ax1, bx1)
    h = min(ay2, by2) - max(ay1, by1)
    overlap = 0
    if w > 0 and h > 0:
        overlap = w * h
    return area_a + area_b - overlap


def main():
    # 一行 8 个数：第一个矩形左下、右上，第二个矩形左下、右上
    a = list(map(int, input().split()))
    print(solve(*a))


if __name__ == "__main__":
    main()
