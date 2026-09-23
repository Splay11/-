def solve(r, c, a):
  # 层和列对调：新表第 j 行第 i 列 = 原表第 i 行第 j 列
  # 新表一共 c 行、r 列
  b = []
  for j in range(c):
    row = []
    for i in range(r):
      row.append(a[i][j])
    b.append(row)
  return b


if __name__ == "__main__":
  # 第一行：层数、列数
  r, c = map(int, input().split())
  a = []
  for _ in range(r):
    a.append(list(map(int, input().split())))
  b = solve(r, c, a)
  # 按新表逐行输出，行内空格分隔
  for row in b:
    print(" ".join(map(str, row)))
