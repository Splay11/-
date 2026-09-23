def solve(n, fa, w, W):
  # 建二叉树：每个点最多两个孩子
  ch = [[] for _ in range(n)]
  for i in range(1, n):
    ch[fa[i - 1]].append(i)

  sz = [1] * n
  sumw = [0.0] * n
  edfn = [0.0] * n

  # 先算子树大小与子树权值和（自底向上）
  order = list(range(n))
  order.reverse()
  for u in order:
    sw = float(w[u])
    s = 1
    for v in ch[u]:
      s += sz[v]
      sw += sumw[v]
    sz[u] = s
    sumw[u] = sw

  # 从根做先序期望：根的 dfn 恒为 1
  edfn[0] = 1.0
  stack = [0]
  while stack:
    u = stack.pop()
    kids = ch[u]
    if len(kids) == 0:
      continue
    if len(kids) == 1:
      # 只有一个孩子，下一名必是它，期望 dfn 比父亲多 1
      v = kids[0]
      edfn[v] = edfn[u] + 1.0
      stack.append(v)
      continue
    # 两个孩子按权值比例决定谁先被整棵子树遍历
    a, b = kids[0], kids[1]
    wa, wb = float(w[a]), float(w[b])
    s = wa + wb
    # 先走兄弟整棵子树，会把对方子树大小加进自己的 dfn
    edfn[a] = edfn[u] + 1.0 + (wb / s) * sz[b]
    edfn[b] = edfn[u] + 1.0 + (wa / s) * sz[a]
    stack.append(a)
    stack.append(b)

  # 原始期望：每个点贡献 (n+1-期望dfn)*权值
  base = 0.0
  for i in range(n):
    base += w[i] * (n + 1.0 - edfn[i])
  best = base

  # 枚举把至多一个点改成 W
  for x in range(n):
    if w[x] == W:
      continue
    # 默认：改权值不改遍历概率（根、独子都是这种情况）
    extra = (W - w[x]) * (n + 1.0 - edfn[x])
    p = fa[x - 1] if x > 0 else -1
    sib = -1
    if p >= 0 and len(ch[p]) == 2:
      a, b = ch[p][0], ch[p][1]
      sib = b if a == x else a
    if sib >= 0:
      # 改的是某个双孩子结点的一侧，会改写兄弟之间的先后概率
      wx, ws = float(w[x]), float(w[sib])
      old_den = wx + ws
      new_den = W + ws
      old_psx = ws / old_den
      new_psx = ws / new_den
      old_pxs = wx / old_den
      new_pxs = W / new_den
      # x 子树里每个人的期望 dfn 变化
      d_x = (new_psx - old_psx) * sz[sib]
      # 兄弟子树里每个人的期望 dfn 变化
      d_s = (new_pxs - old_pxs) * sz[x]
      extra -= d_x * (sumw[x] - w[x] + W)
      extra -= d_s * sumw[sib]
    cand = base + extra
    if cand > best:
      best = cand
  return best


if __name__ == "__main__":
  # 第一行点数；第二行 n-1 个父亲（n=1 时该行为空）；第三行权值；第四行目标权值
  n = int(input())
  fa = list(map(int, input().split()))
  w = list(map(int, input().split()))
  W = int(input())
  print("%.4f" % solve(n, fa, w, W))
