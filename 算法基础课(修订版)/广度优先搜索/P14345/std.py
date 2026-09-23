from collections import deque

def main():
    a, b = map(int, input().split())

    # 如果b小于1，直接输出-1
    if b < 1:
        print(-1)
        return

    # 定义一个数组来记录访问状态，范围到10^6
    visited = [-1] * (1000001)
    q = deque()

    # 从1开始
    q.append(1)
    visited[1] = 0

    while q:
        current = q.popleft()

        # 如果到达目标，输出结果
        if current == b:
            print(visited[current])
            return

        # 第一种魔法：乘以a
        next1 = current * a
        if next1 <= 1000000 and visited[next1] == -1:
            visited[next1] = visited[current] + 1
            q.append(next1)

        # 第二种魔法：循环右移一次
        if current >= 10 and current % 10 != 0:
            rotated = str(current)[-1] + str(current)[:-1]
            next2 = int(rotated)

            if next2 <= 1000000 and visited[next2] == -1:
                visited[next2] = visited[current] + 1
                q.append(next2)

    # 如果无法到达目标，输出-1
    print(-1)

if __name__ == "__main__":
    main()
