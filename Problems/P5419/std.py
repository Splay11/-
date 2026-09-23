# 偶数长度窗口上 0/1 数量相等：交错串 0101... 一定合法


def build_balanced_01(k):
    # 灯位从 1 开始：奇数位放 0，偶数位放 1，得到 0101...
    # 任意偶数长度窗口里奇偶下标各一半，因此 0 和 1 一样多
    chars = []
    for i in range(1, k + 1):
        if i % 2 == 1:
            chars.append("0")
        else:
            chars.append("1")
    return "".join(chars)


def main():
    # 第一行灯带长度，第二行窗口条数
    k = int(input())
    q = int(input())
    # 窗口长度已保证为偶数，交错串对所有窗口都成立，读掉 a,b 即可
    for _ in range(q):
        input()
    print(build_balanced_01(k))


if __name__ == "__main__":
    main()
