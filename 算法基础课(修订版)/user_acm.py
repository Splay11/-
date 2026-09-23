from typing import List
import sys


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        # 请在这里实现
        pass


if __name__ == "__main__":
    data = sys.stdin.read().strip().split()
    n = int(data[0])
    nums = list(map(int, data[1:1 + n]))

    solution = Solution()
    solution.moveZeroes(nums)

    print(" ".join(map(str, nums)))
