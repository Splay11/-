import sys

def main():
    data = sys.stdin.read().strip().split()
    # data: n, m, s, 接着 2*m 个字符
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    s = next(it).strip()

    # 矛盾矩阵
    conflict = [[False]*26 for _ in range(26)]
    for _ in range(m):
        a = next(it)
        b = next(it)
        ia = ord(a) - 65
        ib = ord(b) - 65
        if ia != ib:
            conflict[ia][ib] = True
            conflict[ib][ia] = True

    last = [-1]*26   # 每个字母最近出现位置
    l = 0
    ans = 0

    for r, ch in enumerate(s):
        c = ord(ch) - 65
        # 将 l 推过所有与 c 冲突且在当前窗口内的字母
        for x in range(26):
            if conflict[c][x] and last[x] >= l:
                l = last[x] + 1
        # 以 r 为右端点的和谐子串数
        ans += (r - l + 1)
        # 更新 c 的最近出现位置
        last[c] = r

    print(ans)

if __name__ == "__main__":
    main()
