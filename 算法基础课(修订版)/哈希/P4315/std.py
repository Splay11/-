import sys

def read_all_tokens():
    data = sys.stdin.read().strip().split()
    return data

def main():
    tok = read_all_tokens()
    it = iter(tok)

    T = int(next(it))
    out = []
    for _ in range(T):
        n = int(next(it))
        # 用第一个串初始化最小频次
        s0 = next(it)
        mn = [0]*26
        for ch in s0:
            mn[ord(ch) - 97] += 1

        # 合并其余 n-1 个串的最小频次
        for _ in range(n - 1):
            s = next(it)
            cnt = [0]*26
            for ch in s:
                cnt[ord(ch) - 97] += 1
            for i in range(26):
                if cnt[i] < mn[i]:
                    mn[i] = cnt[i]

        # 构造答案（按字典序最小）
        ans = []
        for i in range(26):
            if mn[i] > 0:
                ans.append(chr(97 + i) * mn[i])
        res = ''.join(ans)
        out.append(res if res else "-1")

    print('\n'.join(out))

if __name__ == "__main__":
    main()
