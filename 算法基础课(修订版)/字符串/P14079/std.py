def main():
    # 输入两个字符串 A 和 B
    A = input().strip()  # 输入字符串 A
    B = input().strip()  # 输入字符串 B

    # 遍历 A 字符串的每个位置，尝试插入 B
    for i in range(len(A) + 1):  # 遍历 A 的所有插入位置，i 从 0 到 len(A)
        # 构造新字符串，将 B 插入到 A 的第 i 个位置
        new_string = A[:i] + B + A[i:]
        
        # 判断新字符串是否为回文
        if new_string == new_string[::-1]:  # 判断回文，x == x[::-1]
            print("YES")
            return  # 找到回文，立即返回

    print("NO")  # 如果没有找到回文，输出 NO

if __name__ == "__main__":
    main()
