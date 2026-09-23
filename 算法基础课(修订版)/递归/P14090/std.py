# 递归函数：反转字符串
def reverse_string(s):
    # 基准条件：如果字符串为空或长度为1，直接返回原字符串
    if len(s) <= 1:
        return s
    # 递归：反转剩余部分，拼接当前字符
    return reverse_string(s[1:]) + s[0]

# 主函数
if __name__ == "__main__":
    s = input()  # 输入字符串
    print(reverse_string(s))  # 输出反转后的字符串
