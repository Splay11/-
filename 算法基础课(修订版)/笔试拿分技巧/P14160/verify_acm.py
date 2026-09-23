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


class Solution:
    def solve(self, a):
        alls = sorted(set(a), reverse=True)
        rank = {v: i + 1 for i, v in enumerate(alls)}
        bit = BIT(len(alls))
        result = 0
        for num in a:
            idx = rank[num]
            total = bit.query(idx - 1)
            res = (total + 1) % MOD
            result = (result + res) % MOD
            bit.add(idx, res)
        return result


if __name__ == "__main__":
    n = int(input())
    a = list(map(int, input().split()))
    solution = Solution()
    print(solution.solve(a))
