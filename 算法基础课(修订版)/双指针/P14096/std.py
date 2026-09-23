def longest_unique_subarray_length(a):
    seen = set()  # 用于记录当前窗口中的元素
    left = 0  # 左指针
    max_length = 0  # 最长不重复子数组的长度

    # 遍历数组
    for right in range(len(a)):
        # 如果当前元素在窗口中已经存在，收缩窗口
        while a[right] in seen:
            seen.remove(a[left])
            left += 1

        # 加入当前元素
        seen.add(a[right])
        
        # 更新最大长度
        max_length = max(max_length, right - left + 1)

    return max_length

# 主函数，读取输入
if __name__ == '__main__':
    n = int(input())  # 读取序列长度
    a = list(map(int, input().split()))  # 读取整数序列

    print(longest_unique_subarray_length(a))
