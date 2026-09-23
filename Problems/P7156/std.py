def solve(gas, cost):
    """环形加油站：若总油量小于总耗油则无解。
    否则从左到右扫一遍，油箱一旦为负就把起点改到下一个站并清空油箱。
    因为可行起点唯一，扫完后留下的起点就是答案。
    """
    total = 0
    tank = 0
    start = 0
    n = len(gas)
    for i in range(n):
        diff = gas[i] - cost[i]
        # total 判断整圈够不够油；tank 判断当前起点走到这里会不会中途没油
        total += diff
        tank += diff
        if tank < 0:
            # 从旧起点到 i 这段永远补不回来，只能从 i+1 重新出发
            start = i + 1
            tank = 0
    # 总油不够则任何起点都会在某一站失败
    if total < 0:
        return -1
    return start


def main():
    # 第一行 n，第二行 n 个加油量，第三行 n 个耗油量，编号从 0 开始
    n = int(input())
    gas = list(map(int, input().split()))
    cost = list(map(int, input().split()))
    print(solve(gas, cost))


if __name__ == "__main__":
    main()
