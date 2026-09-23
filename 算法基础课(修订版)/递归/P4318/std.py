import sys

def dfs(a, start, target, path, ans):
    if target == 0:
        ans.append(path[:])
        return
    for i in range(start, len(a)):
        if i > start and a[i] == a[i - 1]:
            continue  # 同层去重
        if a[i] > target:
            break     # 剪枝
        path.append(a[i])
        dfs(a, i + 1, target - a[i], path, ans)  # 每个数只能用一次
        path.pop()

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    target = int(next(it))

    a.sort()
    ans = []
    dfs(a, 0, target, [], ans)

    ans.sort()  # 字典序升序
    if not ans:
        print("")  # 按题意输出空行
        return
    out_lines = []
    for comb in ans:
        out_lines.append(" ".join(map(str, comb)))
    print("\n".join(out_lines))

if __name__ == "__main__":
    main()
