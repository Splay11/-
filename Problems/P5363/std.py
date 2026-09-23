from collections import deque


def max_depth(t):
    # 空树
    if t == "{}":
        return 0
    # 去掉花括号后按逗号切开层序
    vals = t[1:-1].split(",")
    q = deque()
    q.append(vals[0])
    idx = 1
    depth = 0
    while q:
        # 当前层的每个真实探头都会把深度推进一层
        depth += 1
        sz = len(q)
        for _ in range(sz):
            q.popleft()
            # 层序里接下来至多两个孩子；末尾省略则不再读
            if idx < len(vals):
                left = vals[idx]
                idx += 1
                if left != "#":
                    q.append(left)
            if idx < len(vals):
                right = vals[idx]
                idx += 1
                if right != "#":
                    q.append(right)
    return depth


def main():
    t = input().strip()
    print(max_depth(t))


if __name__ == "__main__":
    main()
