# 排列还原升序的最小交换次数 = n - 环个数

def main():
    n = int(input())
    p = list(map(int, input().split()))
    # p[i] 是位置 i（0-based）上的值；目标位置为值-1
    vis = [False] * n
    cycles = 0
    for i in range(n):
        if vis[i]:
            continue
        # 沿着置换走完一个环
        cycles += 1
        j = i
        while not vis[j]:
            vis[j] = True
            j = p[j] - 1
    # 每个环内部需要 (长度-1) 次交换，总和 = n - 环数
    print(n - cycles)


if __name__ == "__main__":
    main()
