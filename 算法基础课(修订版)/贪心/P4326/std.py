import sys

# 读入多组数据并判定是否能构成 1..n 的排列
def main():
	data = list(map(int, sys.stdin.buffer.read().split()))
	if not data:
		return
	t = data[0]
	idx = 1
	out = []
	for _ in range(t):
		n = data[idx]; idx += 1
		a = data[idx:idx + n]; idx += n
		a.sort(reverse=True)  # 降序
		used = [False] * (n + 1)
		ok = True
		for x in a:
			while x > n or (x > 0 and used[x]):
				x //= 2
			if x == 0:
				ok = False
				break
			used[x] = True
		out.append("YES" if ok else "NO")
	print("\n".join(out))

if __name__ == "__main__":
	main()
