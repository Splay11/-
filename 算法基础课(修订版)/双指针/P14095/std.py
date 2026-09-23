def shortest_all_letters_substring(s):
    # 记录每个字母出现的次数
    count = [0] * 26
    unique = 0  # 当前窗口中不同字母的数量
    n = len(s)
    min_len = n + 1  # 初始值设置为大于可能的最大长度
    left = 0
    
    for right in range(n):
        c = s[right]
        if 'a' <= c <= 'z':  # 仅处理小写字母
            idx = ord(c) - ord('a')
            if count[idx] == 0:
                unique += 1  # 新增一个不同的字母
            count[idx] += 1

        # 当窗口包含所有26个字母时，尝试收缩左边界
        while unique == 26:
            # 更新最小长度
            min_len = min(min_len, right - left + 1)
            cl = s[left]
            if 'a' <= cl <= 'z':
                idx = ord(cl) - ord('a')
                count[idx] -= 1
                if count[idx] == 0:
                    unique -= 1  # 如果移出的是唯一的字母，unique减少
            left += 1  # 收缩窗口

    return min_len if min_len <= n else -1  # 如果找到了符合条件的子串，返回最小长度，否则返回 -1


# 读取输入字符串并调用函数
if __name__ == '__main__':
    s = input().strip()
    print(shortest_all_letters_substring(s))
