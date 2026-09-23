import heapq
import random


class TreapNode:
  __slots__ = ("key", "prio", "left", "right")

  def __init__(self, key):
    self.key = key
    self.prio = random.randrange(1 << 30)
    self.left = None
    self.right = None


def _merge(a, b):
  if not a or not b:
    return a or b
  if a.prio > b.prio:
    a.right = _merge(a.right, b)
    return a
  b.left = _merge(a, b.left)
  return b


def _split(t, key):
  if not t:
    return None, None
  if t.key < key:
    l, r = _split(t.right, key)
    t.right = l
    return t, r
  l, r = _split(t.left, key)
  t.left = r
  return l, t


def _insert_node(t, key):
  if not t:
    return TreapNode(key)
  l, r = _split(t, key)
  return _merge(l, _merge(TreapNode(key), r))


def _erase_node(t, key):
  if not t:
    return None
  l, r = _split(t, key)
  mid, rr = _split(r, key + 1)
  return _merge(l, rr)


def _lower_key(t, key):
  ans = None
  while t:
    if t.key < key:
      ans = t.key
      t = t.right
    else:
      t = t.left
  return ans


def _higher_key(t, key):
  ans = None
  while t:
    if t.key > key:
      ans = t.key
      t = t.left
    else:
      t = t.right
  return ans


def _inorder(t, out):
  if not t:
    return
  _inorder(t.left, out)
  out.append(t.key)
  _inorder(t.right, out)


class GapTracker:
  def __init__(self, vals):
    self.cnt = {}
    self.root = None
    for v in vals:
      self.cnt[v] = self.cnt.get(v, 0) + 1
      if self.cnt[v] == 1:
        self.root = _insert_node(self.root, v)
    self.gap_cnt = {}
    self.gap_heap = []
    keys = []
    _inorder(self.root, keys)
    for i in range(len(keys) - 1):
      self._add_gap(keys[i + 1] - keys[i])

  def _add_gap(self, diff):
    g = diff // 2
    if g > 0:
      self.gap_cnt[g] = self.gap_cnt.get(g, 0) + 1
      heapq.heappush(self.gap_heap, -g)

  def _remove_gap(self, diff):
    g = diff // 2
    if g > 0:
      c = self.gap_cnt.get(g, 0) - 1
      if c == 0:
        del self.gap_cnt[g]
      else:
        self.gap_cnt[g] = c

  def max_g(self):
    while self.gap_heap and -self.gap_heap[0] not in self.gap_cnt:
      heapq.heappop(self.gap_heap)
    return -self.gap_heap[0] if self.gap_heap else 0

  def remove(self, v):
    c = self.cnt[v] - 1
    if c == 0:
      del self.cnt[v]
      pred = _lower_key(self.root, v)
      succ = _higher_key(self.root, v)
      if pred is not None:
        self._remove_gap(v - pred)
      if succ is not None:
        self._remove_gap(succ - v)
      if pred is not None and succ is not None:
        self._add_gap(succ - pred)
      self.root = _erase_node(self.root, v)
    else:
      self.cnt[v] = c

  def insert(self, y):
    if y in self.cnt:
      self.cnt[y] += 1
      return
    pred = _lower_key(self.root, y)
    succ = _higher_key(self.root, y)
    if pred is not None and succ is not None:
      self._remove_gap(succ - pred)
    if pred is not None:
      self._add_gap(y - pred)
    if succ is not None:
      self._add_gap(succ - y)
    self.cnt[y] = 1
    self.root = _insert_node(self.root, y)


def solve(n, b, ops):
  gt = GapTracker(b)
  out = []
  for x, y in ops:
    old = b[x - 1]
    if old != y:
      gt.remove(old)
      gt.insert(y)
      b[x - 1] = y
    out.append(gt.max_g())
  return out


if __name__ == "__main__":
  n, m = map(int, input().split())
  b = list(map(int, input().split()))
  gt = GapTracker(b)
  for _ in range(m):
    x, y = map(int, input().split())
    old = b[x - 1]
    if old != y:
      gt.remove(old)
      gt.insert(y)
      b[x - 1] = y
    print(gt.max_g())
