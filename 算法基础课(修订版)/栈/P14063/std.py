def compute_weight(n):
    """计算整数 n 的十六进制表示中各位数字的和"""
    if n == 0:
        return 0
    s = 0
    while n > 0:
        digit = n & 0xF  # 获取最低四位，即一个十六进制数字
        s += digit
        n >>= 4  # 右移四位，处理下一个十六进制数字
    return s

def main():
    import sys
    # 读取第一个输入，数组的大小 N
    N = int(input())
    
    # 读取第二行的 N 个整数
    arr = list(map(int, input().split()))
    
    # 计算每个元素的权重
    weights = [compute_weight(num) for num in arr]
    
    # 初始化答案数组，默认所有位置为 -1
    answer = [-1] * N
    
    stack = []  # 栈中存储的是元素的索引
    
    # 从右到左遍历数组
    for i in range(N-1, -1, -1):
        # 弹出栈中所有权重小于或等于当前元素权重的元素
        while stack and weights[stack[-1]] <= weights[i]:
            stack.pop()
        # 如果栈不为空，栈顶元素就是右侧第一个权重更大的元素
        if stack:
            answer[i] = stack[-1]
        else:
            answer[i] = -1
        # 将当前元素的索引压入栈中
        stack.append(i)
    
    # 输出结果，以空格分隔
    print(' '.join(map(str, answer)))

if __name__ == "__main__":
    main()
