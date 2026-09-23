def min_cards_and_full_load(segs):
    # 把每项作业拆成两个事件：beg 处占用 +1，fin 处占用 -1
    # 同一时刻必须先减后加，这样首尾相接不会算成重叠
    events = []
    for beg, fin in segs:
        events.append((beg, 1))
        events.append((fin, -1))
    events.sort(key=lambda x: (x[0], x[1]))

    # 第一遍：历史最大占用就是最少需要的加速卡张数
    cur = 0
    mx = 0
    for _, d in events:
        cur += d
        if cur > mx:
            mx = cur

    # 第二遍：占用保持为 mx 的每个时间段，把长度累加起来
    cur = 0
    last = None
    total = 0
    i = 0
    n = len(events)
    while i < n:
        t = events[i][0]
        if last is not None and cur == mx:
            total += t - last
        # 把同一时刻的事件一次性处理完
        while i < n and events[i][0] == t:
            cur += events[i][1]
            i += 1
        last = t
    return mx, total


def main():
    # 四级格式：首行 m，随后每行 fin,beg
    m = int(input())
    segs = []
    for _ in range(m):
        fin, beg = map(int, input().split(","))
        segs.append((beg, fin))
    k, dur = min_cards_and_full_load(segs)
    print(k)
    print(dur)


if __name__ == "__main__":
    main()
