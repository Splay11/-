def solve(n, cons):
  # 带权并查集：把每个量值写成「根变量的一次式」
  # c[x] = sgn[x] * c[root] + off[x]，其中 sgn 只能是 +1 或 -1
  parent = list(range(n + 1))
  sgn = [1] * (n + 1)
  off = [0] * (n + 1)
  # 根变量若已被方程钉死，记在 fixed[root] 里
  fixed = [None] * (n + 1)

  def find(x):
    # 必须迭代压缩：n 最大 1e5，递归会爆栈
    path = []
    while parent[x] != x:
      path.append(x)
      x = parent[x]
    r = x
    # 从靠近根的结点往外压，保证父亲已经接到根上再更新自己
    for v in reversed(path):
      p = parent[v]
      os = sgn[v]
      sgn[v] = os * sgn[p]
      off[v] = off[v] + os * off[p]
      parent[v] = r
    return r

  def add(a, b, ka, val):
    # 加入方程 c[a] + ka * c[b] = val
    # D 对应 ka=-1（差），S 对应 ka=1（和）
    ra, rb = find(a), find(b)
    sa, oa = sgn[a], off[a]
    sb, ob = sgn[b], off[b]
    # 代入一次式后，只剩下根变量：sa*rA + ka*sb*rB = rhs
    rhs = val - oa - ka * ob
    if ra == rb:
      # 同一连通块：变成「系数 * 根 = rhs」
      coef = sa + ka * sb
      if coef == 0:
        # 系数消掉，要么冗余（rhs=0），要么矛盾
        return rhs == 0
      if rhs % coef != 0:
        # 根必须是整数，除不尽就是无整数解
        return False
      need = rhs // coef
      if fixed[ra] is not None and fixed[ra] != need:
        return False
      fixed[ra] = need
      return True
    # 不同连通块：把 ra 挂到 rb，由 sa*rA + ka*sb*rB = rhs 解出 rA
    parent[ra] = rb
    sgn[ra] = -sa * ka * sb
    off[ra] = sa * rhs
    if fixed[ra] is not None and fixed[rb] is not None:
      # 两边都已钉死，检查合并后是否一致
      return fixed[ra] == sgn[ra] * fixed[rb] + off[ra]
    if fixed[ra] is not None:
      # 只知道 rA，反推 rB（sgn 平方为 1）
      fixed[rb] = sgn[ra] * (fixed[ra] - off[ra])
    return True

  for typ, a, b, w in cons:
    ka = -1 if typ == "D" else 1
    if not add(a, b, ka, w):
      return "NO", -1

  # 每个还没被钉死的根，就是一个自由度，各需实测一次
  seen = set()
  k = 0
  for i in range(1, n + 1):
    r = find(i)
    if r not in seen:
      seen.add(r)
      if fixed[r] is None:
        k += 1
  return "YES", k


if __name__ == "__main__":
  # 单组：第一行样品数、记录数，随后每行 D/S u v w
  n, m = map(int, input().split())
  cons = []
  for _ in range(m):
    parts = input().split()
    cons.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))
  ans, k = solve(n, cons)
  print(ans)
  print(k)
