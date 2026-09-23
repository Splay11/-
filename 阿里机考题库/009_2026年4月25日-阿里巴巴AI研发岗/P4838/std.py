def count_leq(load, limit):
    length = len(load)

    # r 为右端点开区间，当前窗口为 [l, r)
    r = 0

    # window_sum 为当前窗口内负载之和
    window_sum = 0

    # cur_score 为当前窗口的段累计分
    cur_score = 0

    cnt = 0

    for l in range(length):
        # 尽量右扩窗口，保证段累计分不超过 limit
        while r < length:
            new_sum = window_sum + load[r]
            new_score = cur_score + new_sum

            if new_score > limit:
                break

            window_sum = new_sum
            cur_score = new_score
            r += 1

        cnt += r - l

        if r > l:
            cur_score -= (r - l) * load[l]
            window_sum -= load[l]
        else:
            r = l + 1

    return cnt


def kth_score(load, rank):
    length = len(load)

    # 上界取整段 [1, length] 的段累计分
    running = 0
    high = 0
    for x in load:
        running += x
        high += running

    low = 0

    # 二分最小的 ans，使 score <= ans 的区间数不少于 rank
    while low < high:
        mid = (low + high) // 2
        if count_leq(load, mid) >= rank:
            high = mid
        else:
            low = mid + 1

    return low


def main():
    tc = int(input())
    for _ in range(tc):
        length, rank = map(int, input().split())
        load = list(map(int, input().split()))
        print(kth_score(load, rank))


if __name__ == "__main__":
    main()
