def solve(n, s, m):
  # 统计 26 种类型各自出现次数
  cnt = [0] * 26
  for ch in s:
    cnt[ord(ch) - 65] += 1
  # 出现次数最多的那种，以及并列最多的种类数
  mx = max(cnt)
  kinds = 0
  for c in cnt:
    if c == mx:
      kinds += 1
  # 用最多种类搭框架：(mx-1) 个完整「处理+冷却」段，最后再放下 kinds 个
  # 若其它单据足够填满空档，答案就是总张数 n
  frame = (mx - 1) * (m + 1) + kinds
  if frame > n:
    return frame
  return n


if __name__ == "__main__":
  # 第一行张数，第二行类型串，第三行冷却长度
  n = int(input())
  s = input().strip()
  m = int(input())
  print(solve(n, s, m))
