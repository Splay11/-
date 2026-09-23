class Solution:
    def maxSubmatrix(self, matrix):
        n = len(matrix)
        m = len(matrix[0])
        # best 记录目前找到的最大总和；br1/bc1/br2/bc2 是它对应的四个坐标
        best = None
        br1 = bc1 = br2 = bc2 = 0

        # 枚举子矩阵的上下边界 r1、r2（共 O(n^2) 对）
        for r1 in range(n):
            # col[j] 表示第 j 列在第 r1 行到当前 r2 行之间的元素之和
            col = [0] * m
            for r2 in range(r1, n):
                row = matrix[r2]
                for j in range(m):
                    col[j] += row[j]

                # 行区间固定后，问题变成一维的「最大子段和」，用 Kadane 求列区间
                cur = 0          # 当前连续列的累加和
                c_start = 0      # 当前连续列的起点
                for j in range(m):
                    if cur <= 0:
                        # 前面的累加和不为正，留着只会拖累结果，从当前列重新开始
                        cur = col[j]
                        c_start = j
                    else:
                        cur += col[j]
                    # 比当前最优更大才更新，保证并列时取先找到的那一个
                    if best is None or cur > best:
                        best = cur
                        br1, bc1, br2, bc2 = r1, c_start, r2, j

        # 返回最优子矩阵的左上角与右下角坐标
        return [br1, bc1, br2, bc2]


def main():
    # 第一行：矩阵行数 N 和列数 M
    n, m = map(int, input().split())
    # 接下来 N 行，每行 M 个整数
    matrix = [list(map(int, input().split())) for _ in range(n)]
    # 输出四个整数：r1 c1 r2 c2
    print(*Solution().maxSubmatrix(matrix))


if __name__ == "__main__":
    main()
