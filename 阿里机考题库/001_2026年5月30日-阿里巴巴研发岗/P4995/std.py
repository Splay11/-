from array import array

def solve_one(z, r):
    a = array("b", (ord(ch) - 97 for ch in z))  # 串 z 转 0..25
    n = len(a)
    done = 0
    hist = []  # 最近至多 26 步的 (哈希, 快照)
    while done < r:
        h = hash(a.tobytes())
        if len(hist) >= 26 and h == hist[-26][0] and hist[-26][1] == a.tobytes():
            # 已进入周期 26：找出会变的位置并跳转
            rem = r - done
            b = array("b", a)
            freq = [0] * 26
            for i in range(n):
                freq[b[i]] += 1
            left = [0] * 26
            ch = []
            for i in range(n):
                c = b[i]
                if left[c] == freq[c] - left[c] - 1:
                    freq[c] -= 1
                    nc = c + 1 if c < 25 else 0
                    b[i] = nc
                    freq[nc] += 1
                    left[nc] += 1
                    ch.append(i)
                else:
                    left[c] += 1
            add = rem % 26
            for i in ch:
                a[i] = (a[i] + add) % 26
            break
        hist.append((h, a.tobytes()))
        if len(hist) > 26:
            hist.pop(0)
        # 做一次变换
        freq = [0] * 26
        for i in range(n):
            freq[a[i]] += 1
        left = [0] * 26
        changed = False
        for i in range(n):
            c = a[i]
            if left[c] == freq[c] - left[c] - 1:
                freq[c] -= 1
                nc = c + 1 if c < 25 else 0
                a[i] = nc
                freq[nc] += 1
                left[nc] += 1
                changed = True
            else:
                left[c] += 1
        done += 1
        if not changed:
            break
    return "".join(chr(x + 97) for x in a)

q = int(input())
for _ in range(q):
    m, r = map(int, input().split())
    z = input().strip()
    print(solve_one(z, r))
