def main():
    # 输入字符串 A 和 B
    A = input().strip()  # 读取字符串 A
    B = input().strip()  # 读取字符串 B
    
    # 计算 A 和 B 的长度
    lenA = len(A)
    lenB = len(B)
    
    # 判断 B 的长度是否是 A 的整数倍
    if lenB % lenA != 0:
        print("No")  # 如果不是，输出 "No"
        return
    
    # 计算重复的次数
    k = lenB // lenA
    constructed = A * k  # 将 A 重复 k 次
    
    # 比较构造的字符串和 B
    if constructed == B:
        print("Yes")  # 如果相等，输出 "Yes"
    else:
        print("No")  # 否则，输出 "No"

if __name__ == "__main__":
    main()
