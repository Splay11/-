def distinct_count(s):
    seen = [False] * 26
    tot = 0
    for ch in s:
        idx = ord(ch) - 97
        if not seen[idx]:
            seen[idx] = True
            tot += 1
    return tot


def can_split(s, m, limit):
    # 每段不同字母不超过 limit 时，最少要拆成几段；能拆得更碎就不会更差
    n = len(s)
    pieces = 0
    i = 0
    while i < n:
        pieces += 1
        if pieces > m:
            return False
        cnt = [0] * 26
        kinds = 0
        j = i
        # 从 i 尽量往右延伸，直到再加一个字母会超过上限
        while j < n:
            idx = ord(s[j]) - 97
            if cnt[idx] == 0:
                if kinds == limit:
                    break
                kinds += 1
            cnt[idx] += 1
            j += 1
        if j == i:
            return False
        i = j
    return True


def min_interference(s, m):
    # 干扰度越大越容易拆进 m 段，二分最小可行上限
    left = 1
    right = distinct_count(s)
    while left < right:
        mid = (left + right) // 2
        if can_split(s, m, mid):
            right = mid
        else:
            left = mid + 1
    return left


def main():
    # 第一行 n、m，第二行报文
    parts = list(map(int, input().split()))
    n = parts[0]
    m = parts[1]
    s = input().strip()
    print(min_interference(s[:n], m))


if __name__ == "__main__":
    main()
