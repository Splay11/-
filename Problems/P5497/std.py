def find_root(parent, delta, x):
    # 找到根，并把途中点的差额改成相对根：delta[x] = 付款[x] - 付款[根]
    if parent[x] != x:
        root = find_root(parent, delta, parent[x])
        delta[x] += delta[parent[x]]
        parent[x] = root
        return root
    return x


def process(n, k, floor_of, queries):
    parent = list(range(n + 1))
    # delta[x]：x 比当前父亲多付的钱；路径压缩后变成比根多付的钱
    delta = [0] * (n + 1)
    sz = [1] * (n + 1)
    invalid = 0
    for a, b, x in queries:
        # 自己跟自己比，差额只能是 0
        if a == b:
            if x != 0:
                invalid += 1
            continue
        ra = find_root(parent, delta, a)
        rb = find_root(parent, delta, b)
        if ra == rb:
            # 两人已在同一圈：推出的差额必须正好是 x
            if delta[a] - delta[b] != x:
                invalid += 1
            continue
        # 不同圈：楼层不同或合并后人数超 K，本条作废
        if floor_of[a] != floor_of[b] or sz[ra] + sz[rb] > k:
            invalid += 1
            continue
        # 记下 pay[a] - pay[b] = x，小圈挂到大圈下面
        if sz[ra] < sz[rb]:
            parent[ra] = rb
            delta[ra] = x - delta[a] + delta[b]
            sz[rb] += sz[ra]
        else:
            parent[rb] = ra
            delta[rb] = delta[a] - delta[b] - x
            sz[ra] += sz[rb]
    # 还没被挂到别人下面的点，就是还在的结算圈
    circles = 0
    for i in range(1, n + 1):
        if parent[i] == i:
            circles += 1
    return invalid, circles


def main():
    # 第一行 n、发言数 q、人数上限 K
    parts = list(map(int, input().split()))
    n = parts[0]
    q = parts[1]
    k = parts[2]
    # 第二行各同学楼层，下标从 1 开始
    vals = list(map(int, input().split()))
    floor_of = [0] + vals[:n]
    queries = []
    for _ in range(q):
        a, b, x = map(int, input().split())
        queries.append((a, b, x))
    invalid, circles = process(n, k, floor_of, queries)
    print(invalid)
    print(circles)


if __name__ == "__main__":
    main()
