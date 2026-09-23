def solve(pids, ppids, kill):
    """从 kill 出发走完整棵子树，把所有会被杀掉的进程收集起来再排序。
    用栈做 DFS，n 可以到 5e4，链状树递归会爆。
    """
    # 先给每个进程准备一个孩子列表
    children = {}
    for p in pids:
        children[p] = []
    for child, parent in zip(pids, ppids):
        # 父进程为 0 的是根，没有人再指向它的父亲
        if parent != 0:
            children[parent].append(child)
    killed = []
    stack = [kill]
    while stack:
        u = stack.pop()
        killed.append(u)
        # 杀掉 u 时，它的所有孩子也会被杀掉
        for v in children[u]:
            stack.append(v)
    # 题面要求按进程 ID 从小到大输出
    killed.sort()
    return killed


def main():
    # 第一行：进程数 n、要终止的进程 kill
    n, kill = map(int, input().split())
    pids = list(map(int, input().split()))
    ppids = list(map(int, input().split()))
    ans = solve(pids, ppids, kill)
    print(" ".join(str(x) for x in ans))


if __name__ == "__main__":
    main()
