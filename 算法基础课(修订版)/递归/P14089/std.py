# 递归函数计算斐波那契数列
def fibonacci(n):
    if n == 0:
        return 0  # 斐波那契数列的第0项
    if n == 1:
        return 1  # 斐波那契数列的第1项
    return fibonacci(n - 1) + fibonacci(n - 2)  # 递归计算F(n)

# 主函数
if __name__ == "__main__":
    n = int(input())  # 输入整数n
    print(fibonacci(n))  # 输出斐波那契数列的第n项
