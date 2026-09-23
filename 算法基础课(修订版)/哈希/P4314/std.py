import sys

def main():
    n = int(sys.stdin.readline().strip())
    s = sys.stdin.readline().strip()

    freq = [0] * 26
    tot = 0
    wrap = 0
    res = []

    for i, ch in enumerate(s, 1):
        tot += i                 # 前缀子串总数增加 i
        k = ord(ch) - 97
        wrap += freq[k] + 1      # 新增包裹子串数量
        freq[k] += 1
        res.append(str(tot - wrap))

    print("\n".join(res))

if __name__ == "__main__":
    main()
