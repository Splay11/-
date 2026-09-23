# 有向欧拉路径：从 Core-SW-01 出发，每条跳转恰好一次，字典序最小。

START = "Core-SW-01"


def find_path(hops):
    g = {}
    for u, v in hops:
        if u not in g:
            g[u] = []
        g[u].append(v)
    for u in g:
        g[u].sort(reverse=True)
    route = []
    stack = [START]
    while stack:
        u = stack[-1]
        vs = g.get(u)
        if vs:
            # 出边已按终点名字从大到小排，弹出末尾就是当前更小的终点
            # 有未用跳转就继续往前走，把终点压栈
            # 没有出边才记下当前点，相当于后序，死胡同会先出现在答案尾部
            # 这样不会像纯贪心那样走进死胡同就再也回不来
            stack.append(vs.pop())
        else:
            route.append(u)
            stack.pop()
    route.reverse()
    return route


def main():
    hops = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        line = line.strip()
        if not line:
            continue
        u, v = line.split()
        hops.append((u, v))
    ans = find_path(hops)
    print(" ".join(ans))


if __name__ == "__main__":
    main()
