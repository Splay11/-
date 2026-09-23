# 把下标闭区间 [l, r] 内每个字符同时后继 k 次（z 的后继是 a）
def shift_range(chars, l, r, k):
  for i in range(l, r + 1):
    chars[i] = chr((ord(chars[i]) - 97 + k) % 26 + 97)


def solve(n, s):
  chars = list(s)
  # 左边已经是 z 的位置不必动：再后继会变成 a，字典序立刻变差
  i = 0
  while i < n and chars[i] == "z":
    i += 1
  # 全是 z，只能得到原串
  if i == n:
    return s
  # 让第一个非 z 变成 z，整段必须加同一个步数
  k = ord("z") - ord(chars[i])
  j = i
  # 向右延伸到「再纳入就会越过 z」的前一个位置，避免某位变成很小的字母
  while j < n and ord(chars[j]) + k <= ord("z"):
    j += 1
  shift_range(chars, i, j - 1, k)
  return "".join(chars)


if __name__ == "__main__":
  n = int(input())
  s = input().strip()
  print(solve(n, s))
