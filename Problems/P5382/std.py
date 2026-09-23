# 沿当前方向扫描，能揭就揭；整趟没有进展则失败，否则掉头继续


def min_turns(w):
    n = len(w)
    opened = [False] * n
    keys = 0
    done = 0
    ans = 0
    d = 1
    i = 0
    while done < n:
        gained = 0
        # 沿当前方向走到尽头，路过能揭的彩门就揭
        while 0 <= i < n:
            if (not opened[i]) and keys >= w[i]:
                opened[i] = True
                keys += 1
                done += 1
                gained += 1
            i += d
        if done == n:
            return ans
        # 这一趟一扇都没揭开，剩下的阈值永远够不着
        if gained == 0:
            return -1
        # 走到尽头后换向，从端点外再踏回数组
        d = -d
        i += d
        ans += 1
    return ans


def main():
    q = int(input())
    for _ in range(q):
        n = int(input())
        w = list(map(int, input().split()))
        print(min_turns(w))


if __name__ == "__main__":
    main()
