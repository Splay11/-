import sys


# 计算每个位置是否可行
def solve_array(v):
    n = len(v)
    M = max(v)  # 序列最大值

    # 二进制字典树：ch0[x]、ch1[x] 分别表示节点 x 的 0/1 儿子，-1 表示不存在
    ch0 = [-1]
    ch1 = [-1]

    def insert(x):
        # 将一个读数插入二进制字典树
        node = 0
        for b in range(30, -1, -1):
            bit = (x >> b) & 1
            if bit == 0:
                if ch0[node] == -1:
                    ch0[node] = len(ch0)
                    ch0.append(-1)
                    ch1.append(-1)
                node = ch0[node]
            else:
                if ch1[node] == -1:
                    ch1[node] = len(ch1)
                    ch0.append(-1)
                    ch1.append(-1)
                node = ch1[node]

    def query_max_xor(x):
        # 查询与 x 异或能得到的最大值
        node = 0
        res = 0
        for b in range(30, -1, -1):
            bit = (x >> b) & 1
            # 优先走相反位，使当前位异或结果为 1
            if bit == 0:
                if ch1[node] != -1:
                    res |= 1 << b
                    node = ch1[node]
                else:
                    node = ch0[node]
            else:
                if ch0[node] != -1:
                    res |= 1 << b
                    node = ch0[node]
                else:
                    node = ch1[node]
        return res

    ans = ['0'] * n

    # 从右往左维护后缀字典树
    for i in range(n - 1, -1, -1):
        if i < n - 1:
            best = query_max_xor(v[i])
            if best >= M:
                ans[i] = '1'

        # 当前读数插入，供左侧位置查询
        insert(v[i])

    return ''.join(ans)


def main():
    input = sys.stdin.readline
    n = int(input())
    v = list(map(int, input().split()))
    print(solve_array(v))


if __name__ == "__main__":
    main()
