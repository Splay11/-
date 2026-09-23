# 分苹果：回溯枚举每人分到的个数，保证总和为 m，按字典序输出

def dfs(remain, idx, n, path, schemes):
    # idx 为当前要分配的人（0-based），remain 为剩余苹果
    if idx == n - 1:
        # 最后一人必须拿完剩余苹果
        path.append(remain)
        schemes.append(path[:])
        path.pop()
        return
    # 当前人可拿 0..remain，从小到大保证字典序
    for x in range(remain + 1):
        path.append(x)
        dfs(remain - x, idx + 1, n, path, schemes)
        path.pop()


def main():
    m, n = map(int, input().split())
    schemes = []
    dfs(m, 0, n, [], schemes)
    for s in schemes:
        print(" ".join(map(str, s)))
    print(len(schemes))


if __name__ == "__main__":
    main()
