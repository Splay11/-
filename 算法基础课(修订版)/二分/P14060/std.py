def check(a, b, c, mid):
    a1, b1, c1 = a, b, c

    # 尝试从红砖合成蓝砖
    if a1 > mid:
        f = (a1 - mid) // x  # 计算多余的红砖能合成多少蓝砖
        a1 -= x * f  # 消耗掉这些红砖
        b1 += f  # 增加蓝砖的数量

    # 尝试从蓝砖合成绿砖
    if b1 > mid:
        f = (b1 - mid) // y  # 计算多余的蓝砖能合成多少绿砖
        b1 -= y * f  # 消耗掉这些蓝砖
        c1 += f  # 增加绿砖的数量

    return a1 >= mid and b1 >= mid and c1 >= mid

# 读取测试数据的组数
T = int(input())

# 遍历每一组数据
for _ in range(T):
    # 读取每组数据
    a, b, c, x, y = map(int, input().split())

    # 二分查找的左边界和右边界
    l = 0
    r = 10**9

    # 二分查找
    while l < r:
        mid = (l + r + 1) // 2  # 尝试获取的中间套数
        
        # 如果经过合成后，红砖、蓝砖、绿砖都能满足mid套，则可以尝试更大的mid
        if check(a, b, c, mid):
            l = mid
        else:
            r = mid - 1  # 否则尝试更小的mid

    # 输出结果，即最多可以收集到的砖块套数
    print(l)
