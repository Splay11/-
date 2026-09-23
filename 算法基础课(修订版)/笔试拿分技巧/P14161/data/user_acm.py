class Solution:
    def solve(self, times, mutex_pairs):
        # 请在这里实现
        return 0


if __name__ == "__main__":
    job_num = int(input())
    times = list(map(int, input().split()))
    mutex_num = int(input())
    mutex_pairs = []
    for _ in range(mutex_num):
        a, b = map(int, input().split())
        mutex_pairs.append((a, b))

    solution = Solution()
    print(solution.solve(times, mutex_pairs))
