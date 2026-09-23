def solve(n, a):
  # 从左到右扫：左边按过的次数决定当前位被翻转了几次
  ans = 0
  flip = 0
  for x in a:
    # 当前实际状态 = 初值异或「左边已按次数的奇偶」
    cur = x ^ flip
    if cur == 0:
      # 离开前必须按一次，否则这盏灯再也改不回来
      ans += 1
      flip ^= 1
  return ans


if __name__ == "__main__":
  # 第一行长度，第二行 0/1 序列
  n = int(input())
  a = list(map(int, input().split()))
  print(solve(n, a))
