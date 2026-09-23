def eliminate_game(arr):
    stack = []  # 创建一个空栈

    # 遍历数组中的每个元素
    for num in arr:
        stack.append(num)  # 将当前元素压入栈中

        # 每次插入新元素后，检查栈顶是否有三个相同的元素
        if len(stack) >= 3 and stack[-1] == stack[-2] == stack[-3]:
            # 如果有三个相同的元素，弹出这三个元素
            stack.pop()  # 弹出栈顶元素
            stack.pop()  # 弹出栈顶元素
            stack.pop()  # 弹出栈顶元素

    # 构建结果数组
    return stack  # 返回栈中剩余的元素

def main():
    # 输入一行数据
    arr = list(map(int, input().split()))

    # 调用消除函数
    result = eliminate_game(arr)

    # 输出结果
    if not result:
        print("[]")  # 如果栈为空，输出空数组
    else:
        print(" ".join(map(str, result)))  # 输出栈中的元素

if __name__ == "__main__":
    main()
