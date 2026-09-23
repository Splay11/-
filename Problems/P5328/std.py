def solve(k, v):
  # 贪心：货一到就入栈，栈顶刚好是下一个该出的号就立刻出
  st = []
  ops = []
  need = 1
  for x in v:
    st.append(x)
    ops.append("I")
    while st and st[-1] == need:
      st.pop()
      ops.append("O")
      need += 1
  if need == k + 1:
    return "".join(ops)
  return "N"


k = int(input())
v = list(map(int, input().split()))
print(solve(k, v))
