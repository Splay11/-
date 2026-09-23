# 截图中的双指针：和等于 k 则左右都移动，和偏小则左移，和偏大则右移


class Solution:
    def twoSum2(self, nums, k):
        left = 0
        right = len(nums) - 1
        count = 0
        # 数组有序且无重复，左右夹逼统计和为 k 的数对
        while left < right:
            current_sum = nums[left] + nums[right]
            if current_sum == k:
                # 找到一对，两侧都收一格；无重复所以不会再配同一对数
                count += 1
                left += 1
                right -= 1
            elif current_sum < k:
                # 当前和偏小，左端右移让 nums[left] 变大
                left += 1
            else:
                # 当前和偏大，右端左移让 nums[right] 变小
                right -= 1
        return count


def main():
    n, k = map(int, input().split())
    nums = list(map(int, input().split()))
    print(Solution().twoSum2(nums, k))


if __name__ == "__main__":
    main()
