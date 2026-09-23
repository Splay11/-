class Solution:
    def solve(self, matrix, x1, y1, x2, y2):
        x1 -= 1
        y1 -= 1
        x2 -= 1
        y2 -= 1
        max_val = matrix[x1][y1]
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                max_val = max(max_val, matrix[i][j])
        return max_val


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
