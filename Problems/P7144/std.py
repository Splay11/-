def solve(s):
    """扫一遍，把连续元音段记下来。
    只在更长时更新答案，这样同样长度时保留最先出现的一段。
    全程没有元音则返回 -1。
    """
    vowels = set("aeiou")
    best = ""
    n = len(s)
    i = 0
    while i < n:
        if s[i] not in vowels:
            # 辅音直接跳过；y 也不算元音
            i += 1
            continue
        j = i
        while j < n and s[j] in vowels:
            j += 1
        # 严格更长才更新，平局保留左边那段
        if j - i > len(best):
            best = s[i:j]
        i = j
    if not best:
        return "-1"
    return best


def main():
    # 一整行小写字母
    s = input()
    print(solve(s))


if __name__ == "__main__":
    main()
