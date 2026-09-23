# 读取输入
s = input().strip()  # 输入括号字符串
stack = []  # 创建一个栈

# 遍历字符串
for char in s:
    if char == '(':  # 遇到左括号，将其压入栈
        stack.append(char)
    elif char == ')':  # 遇到右括号
        if not stack:  # 如果栈为空，说明没有匹配的左括号
            print("No")
            exit(0)  # 立即结束程序
        stack.pop()  # 弹出栈顶元素，匹配对应的左括号

# 如果栈为空，说明所有的左括号都有匹配
if not stack:
    print("Yes")  # 如果栈为空，输出 Yes
else:
    print("No")  # 如果栈不为空，输出 No
