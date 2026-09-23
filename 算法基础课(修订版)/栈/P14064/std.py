maxn = 1010  # 最大栈大小，足够容纳输入的所有数
stack = [0] * maxn  # 用数组模拟栈，初始化栈的大小为maxn
top = 0  # 栈顶指针，表示栈中最后一个有效元素的位置

arr = list(map(int, input().split()))  # 读取输入的数字并转换为列表

# 遍历输入的每个数
for x in arr:
    # 尝试合并栈内元素直到不满足合并条件
    while True:
        flag = False  # 用来标记是否执行了合并操作
        tmp = 0  # 用来存储当前连续栈内元素的和
        
        # 从栈顶开始向下遍历所有元素
        for i in range(top, -1, -1):
            tmp += stack[i]  # 累加栈中的元素
            
            # 如果当前连续元素的和等于当前的x
            if tmp == x:
                # 合并栈内元素，设置新的x值为当前和的两倍
                x += tmp
                # 更新栈顶，i-1表示将合并的元素出栈
                top = i - 1
                flag = True  # 标记已经合并
                break  # 跳出当前for循环
        
        # 如果没有合并任何元素，跳出while循环
        if not flag:
            break
    
    # 将当前x压入栈中
    top += 1  # 栈顶位置增加
    stack[top] = x  # 将x放入栈顶位置

# 输出栈中的所有元素（从栈顶开始打印）
while top > 0:
    print(stack[top], end=" ")  # 输出栈顶元素
    top -= 1  # 栈顶指针向下移动
