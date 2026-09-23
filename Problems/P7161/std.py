def solve(words):
    """统计每个小写字母在所有字符串里出现次数的最小值。
    最小值为 k 就把该字母输出 k 次，再按字典序排好。
    """
    min_cnt = [10**9] * 26
    for w in words:
        cnt = [0] * 26
        for ch in w:
            cnt[ord(ch) - 97] += 1
        for i in range(26):
            if cnt[i] < min_cnt[i]:
                min_cnt[i] = cnt[i]
    chars = []
    for i in range(26):
        # 按 a..z 顺序重复输出 min 次
        for _ in range(min_cnt[i]):
            chars.append(chr(97 + i))
    return chars


def main():
    # 第一行 n，随后 n 行每个字符串
    n = int(input())
    words = []
    for _ in range(n):
        words.append(input().strip())
    chars = solve(words)
    print(len(chars))
    # 没有公共字符时只输出 0，不再打第二行
    if chars:
        print(" ".join(chars))


if __name__ == "__main__":
    main()
