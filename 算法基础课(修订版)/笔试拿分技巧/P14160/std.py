MOD = 10**9 + 7

class BIT:
    def __init__(self, n):
        self.size = n
        self.tree = [0] * (n + 1)

    def add(self, x, value):
        while x <= self.size:
            self.tree[x] = (self.tree[x] + value) % MOD
            x += x & -x

    def query(self, x):
        res = 0
        while x > 0:
            res = (res + self.tree[x]) % MOD
            x -= x & -x
        return res

def main():
    n = int(input())
    a = list(map(int, input().split()))
    
    alls = sorted(set(a), reverse=True)  # 降序排列并去重
    rank = {v: i + 1 for i, v in enumerate(alls)}  # 离散化映射

    bit = BIT(len(alls))
    result = 0
    
    for num in a:
        id = rank[num]  # 获取离散化后的位置
        sum_ = bit.query(id - 1)  # 查询比当前数小的所有子序列数
        res = (sum_ + 1) % MOD  # 当前元素也可以作为一个长度为1的子序列
        result = (result + res) % MOD
        bit.add(id, res)  # 更新树状数组

    print(result)

if __name__ == "__main__":
    main()
