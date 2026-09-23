q = int(input())
for _ in range(q):
    m, t = map(int, input().split())
    out = []
    # 剩余数字 1..s，s 从 m 降到 1
    s = m
    while s >= 1:
        if t >= s - 1 and s > 1:
            # 放下最大值，贡献 s-1 个逆序对
            out.append(s)
            t -= s - 1
            s -= 1
        else:
            # 剩余段一次性构造出恰好 t 个逆序对
            if t == 0:
                out.extend(range(1, s + 1))
            else:
                out.append(t + 1)
                out.extend(range(1, t + 1))
                out.extend(range(t + 2, s + 1))
            break
    print(*out)
