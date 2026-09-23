class Solution:
    def kthLargestNumber(self, nums, k):
        # 排序键取 (长度, 字符串本身)，并倒序排，等价于「先按数值从大到小排」：
        # reverse=True 时先按长度从大到小，长度相同的再按字典序从大到小
        ordered = sorted(nums, key=lambda s: (len(s), s), reverse=True)
        # 第 k 大对应排序后下标 k-1（重复元素各自占一个名次，无需去重）
        return ordered[k - 1]


def main():
    # 第一行：n（数组长度）和 k（排名）
    n, k = map(int, input().split())
    # 第二行：n 个表示非负整数的字符串
    nums = input().split()
    # 输出第 k 大的那个字符串
    print(Solution().kthLargestNumber(nums, k))


if __name__ == "__main__":
    main()
