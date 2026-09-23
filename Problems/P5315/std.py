def solve(p, s, r):
  # 找每个位置左边、右边最近的「大于等于自己」的下标
  left = [-1] * p
  st = []
  for i in range(p):
    # 栈里保持读数单调不增，栈顶就是左边最近的不低于 r[i] 的位置
    while st and r[st[-1]] < r[i]:
      st.pop()
    if st:
      left[i] = st[-1]
    st.append(i)
  right = [p] * p
  st = []
  for i in range(p - 1, -1, -1):
    while st and r[st[-1]] < r[i]:
      st.pop()
    if st:
      right[i] = st[-1]
    st.append(i)
  peaks = []
  for i in range(p):
    # 半径 s 内不能出现 >= r[i] 的其他测站
    ok_l = left[i] < 0 or i - left[i] > s
    ok_r = right[i] >= p or right[i] - i > s
    if ok_l and ok_r:
      peaks.append(i + 1)
  return peaks


p, s = map(int, input().split())
r = list(map(int, input().split()))
peaks = solve(p, s, r)
print(len(peaks))
print(" ".join(str(x) for x in peaks))
