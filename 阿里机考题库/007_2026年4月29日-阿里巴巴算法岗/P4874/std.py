import sys


# 计算最早空闲时刻：排序维护窗口后，找第一个不被任何窗口覆盖的非负整数
def find_earliest_free(windows):
    # 按窗口起点从小到大排序
    windows.sort()

    # ans 表示当前最早可能空闲的时刻
    ans = 0

    for s, e in windows:
        # 若当前窗口起点大于 ans，说明 ans 未被占用，即为答案
        if s > ans:
            break

        # 若 ans 落在当前窗口内，则把 ans 推进到窗口终点之后
        if e >= ans:
            ans = e + 1

    return ans


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])

    windows = []
    idx = 1

    # 读取 n 个维护窗口
    for _ in range(n):
        s = int(data[idx])
        e = int(data[idx + 1])
        idx += 2
        windows.append((s, e))

    print(find_earliest_free(windows))


if __name__ == "__main__":
    main()
