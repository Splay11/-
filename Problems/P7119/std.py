class Solution:
    def pivotIndex(self, nums):
        # 整个数组的总和，用来 O(1) 推出某个位置右侧的元素之和
        total = sum(nums)
        # left_sum 表示当前下标左侧所有元素之和；下标 0 的左侧没有元素，所以初值为 0
        left_sum = 0
        for i, x in enumerate(nums):
            # 右侧元素之和 = 总和 - 左侧和 - 当前元素本身
            # （当前元素是中心下标所指的元素，既不算左侧也不算右侧）
            if left_sum == total - left_sum - x:
                # 从前往后扫描，第一个满足条件的位置就是最靠左的中心下标
                return i
            # 当前位置不是中心下标，把它累加进左侧，继续考察下一个位置
            left_sum += x
        # 扫完整个数组都没有找到，说明不存在中心下标
        return -1


def main():
    # 第一行：数组长度 n
    n = int(input())
    # 第二行：n 个整数，相邻之间用空格分隔
    nums = list(map(int, input().split()))
    # 输出最靠左的中心下标，不存在则为 -1
    print(Solution().pivotIndex(nums))


if __name__ == "__main__":
    main()
