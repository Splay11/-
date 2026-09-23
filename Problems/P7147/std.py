def solve(asteroids):
    """用栈模拟碰撞：只有栈顶向右、当前向左才会撞。
    当前更大就弹出栈顶继续撞；一样大就双方爆炸；栈顶更大则当前爆炸。
    同向或背向飞走的都不会撞。
    """
    stack = []
    for x in asteroids:
        alive = True
        # 只有「右行遇上左行」才会碰撞
        while alive and stack and stack[-1] > 0 and x < 0:
            top = stack[-1]
            if abs(top) < abs(x):
                # 栈顶更小，炸掉栈顶，当前小行星继续往左撞
                stack.pop()
                continue
            if abs(top) == abs(x):
                # 一样大，两颗一起炸
                stack.pop()
            # 栈顶更大或已经同归于尽，当前这颗不再存活
            alive = False
        if alive:
            stack.append(x)
    return stack


def main():
    # 第一行 n，第二行 n 个非零整数
    n = int(input())
    asteroids = list(map(int, input().split()))
    rest = solve(asteroids)
    print(len(rest))
    # 没有剩余时只输出 0，不要再打空的第二行
    if rest:
        print(" ".join(str(x) for x in rest))


if __name__ == "__main__":
    main()
