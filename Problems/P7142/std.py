def solve(path):
    """用栈按段处理 Unix 路径。
    空段和 . 表示当前目录，直接跳过；.. 表示回上一级，栈非空就弹出；
    其他名字（包括 ...）都是普通目录，压栈。
    """
    stack = []
    for part in path.split("/"):
        if part == "" or part == ".":
            # 连续斜杠会产生空段；单独一个点表示当前目录
            continue
        if part == "..":
            # 已经在根目录时不能再往上走
            if stack:
                stack.pop()
        else:
            stack.append(part)
    if not stack:
        return "/"
    # 目录之间只留一个斜杠，非根路径末尾不加斜杠
    return "/" + "/".join(stack)


def main():
    # 读入一整行绝对路径，再输出规范路径
    path = input()
    print(solve(path))


if __name__ == "__main__":
    main()
