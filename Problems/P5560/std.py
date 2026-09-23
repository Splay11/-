def solve(w, ops):
    # 开符记 +1，合符记 -1。配平 <=> 区间和为 0 且最小前缀和 >= 0
    n = len(w)
    base = 1
    while base < n:
        base <<= 1
    height = base.bit_length() - 1
    # 叶子放在 base 起的位置，凑不满的叶子保持 0，询问范围不会落到那里
    sm = [0] * (base << 1)
    mn = [0] * (base << 1)
    mx = [0] * (base << 1)
    lz = [0] * (base << 1)
    for i, ch in enumerate(w):
        v = 1 if ch == "[" else -1
        leaf = base + i
        sm[leaf] = mn[leaf] = mx[leaf] = v
    for p in range(base - 1, 0, -1):
        left = p << 1
        right = left | 1
        ls = sm[left]
        sm[p] = ls + sm[right]
        mn[p] = mn[left] if mn[left] < ls + mn[right] else ls + mn[right]
        mx[p] = mx[left] if mx[left] > ls + mx[right] else ls + mx[right]

    ans = []
    for op, a, b in ops:
        if op == 1:
            # 对调 [a, b]：先把路径上的懒标记推下去，再覆盖这一段，最后向上重算
            # 1 起编号的闭区间 [a, b] 对应叶子 [base+a-1, base+b)
            left = base + a - 1
            right = base + b
            idx = left
            for shift in range(height, 0, -1):
                p = idx >> shift
                if lz[p]:
                    c = p << 1
                    sm[c] = -sm[c]
                    mn[c], mx[c] = -mx[c], -mn[c]
                    lz[c] ^= 1
                    c |= 1
                    sm[c] = -sm[c]
                    mn[c], mx[c] = -mx[c], -mn[c]
                    lz[c] ^= 1
                    lz[p] = 0
            idx = right - 1
            for shift in range(height, 0, -1):
                p = idx >> shift
                if lz[p]:
                    c = p << 1
                    sm[c] = -sm[c]
                    mn[c], mx[c] = -mx[c], -mn[c]
                    lz[c] ^= 1
                    c |= 1
                    sm[c] = -sm[c]
                    mn[c], mx[c] = -mx[c], -mn[c]
                    lz[c] ^= 1
                    lz[p] = 0
            begin_l = left
            begin_r = right
            while left < right:
                if left & 1:
                    sm[left] = -sm[left]
                    mn[left], mx[left] = -mx[left], -mn[left]
                    lz[left] ^= 1
                    left += 1
                if right & 1:
                    right -= 1
                    sm[right] = -sm[right]
                    mn[right], mx[right] = -mx[right], -mn[right]
                    lz[right] ^= 1
                left >>= 1
                right >>= 1
            # 父亲若仍挂着对调标记，用孩子重算后再把标记作用回去
            idx = begin_l
            while idx > 1:
                idx >>= 1
                leftc = idx << 1
                rightc = leftc | 1
                ls = sm[leftc]
                sm[idx] = ls + sm[rightc]
                mn[idx] = mn[leftc] if mn[leftc] < ls + mn[rightc] else ls + mn[rightc]
                mx[idx] = mx[leftc] if mx[leftc] > ls + mx[rightc] else ls + mx[rightc]
                if lz[idx]:
                    sm[idx] = -sm[idx]
                    mn[idx], mx[idx] = -mx[idx], -mn[idx]
            idx = begin_r - 1
            while idx > 1:
                idx >>= 1
                leftc = idx << 1
                rightc = leftc | 1
                ls = sm[leftc]
                sm[idx] = ls + sm[rightc]
                mn[idx] = mn[leftc] if mn[leftc] < ls + mn[rightc] else ls + mn[rightc]
                mx[idx] = mx[leftc] if mx[leftc] > ls + mx[rightc] else ls + mx[rightc]
                if lz[idx]:
                    sm[idx] = -sm[idx]
                    mn[idx], mx[idx] = -mx[idx], -mn[idx]
        else:
            # 询问 [a, b] 的区间和与最小前缀和
            # 1 起编号的闭区间 [a, b] 对应叶子 [base+a-1, base+b)
            left = base + a - 1
            right = base + b
            idx = left
            for shift in range(height, 0, -1):
                p = idx >> shift
                if lz[p]:
                    c = p << 1
                    sm[c] = -sm[c]
                    mn[c], mx[c] = -mx[c], -mn[c]
                    lz[c] ^= 1
                    c |= 1
                    sm[c] = -sm[c]
                    mn[c], mx[c] = -mx[c], -mn[c]
                    lz[c] ^= 1
                    lz[p] = 0
            idx = right - 1
            for shift in range(height, 0, -1):
                p = idx >> shift
                if lz[p]:
                    c = p << 1
                    sm[c] = -sm[c]
                    mn[c], mx[c] = -mx[c], -mn[c]
                    lz[c] ^= 1
                    c |= 1
                    sm[c] = -sm[c]
                    mn[c], mx[c] = -mx[c], -mn[c]
                    lz[c] ^= 1
                    lz[p] = 0
            left_parts = []
            right_parts = []
            while left < right:
                if left & 1:
                    left_parts.append(left)
                    left += 1
                if right & 1:
                    right -= 1
                    right_parts.append(right)
                left >>= 1
                right >>= 1
            total = 0
            best = None
            for p in left_parts:
                cand = total + mn[p]
                if best is None or cand < best:
                    best = cand
                total += sm[p]
            for j in range(len(right_parts) - 1, -1, -1):
                p = right_parts[j]
                cand = total + mn[p]
                if best is None or cand < best:
                    best = cand
                total += sm[p]
            ans.append(1 if total == 0 and best >= 0 else 0)
    return ans


def main():
    m = int(input())
    t = int(input())
    w = input().strip()
    ops = []
    for _ in range(t):
        op, a, b = map(int, input().split())
        ops.append((op, a, b))
    for bit in solve(w, ops):
        print(bit)


if __name__ == "__main__":
    main()
