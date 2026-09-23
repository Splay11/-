class Solution:
    def solve(self, matrix, x1, y1, x2, y2):
        # 请在这里实现
        return 0


if __name__ == "__main__":
    n, m = map(int, input().split())
    matrix = []
    for _ in range(n):
        matrix.append(list(map(int, input().split())))

    q = int(input())
    solution = Solution()
    for _ in range(q):
        x1, y1, x2, y2 = map(int, input().split())
        print(solution.solve(matrix, x1, y1, x2, y2))
