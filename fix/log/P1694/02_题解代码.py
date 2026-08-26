import bisect, sys
def main():
    data = list(map(int, sys.stdin.read().split()))
    n, a = data[0], data[1:]
    b = sorted(a)
    pref = [0]
    for x in b:
        pref.append(pref[-1] + x)
    out = []
    for x in a:
        i = bisect.bisect_left(b, x)
        j = bisect.bisect_right(b, x)
        ans = x * i - pref[i] + (pref[n] - pref[j]) - x * (n - j)
        out.append(str(ans))
    print("\n".join(out))
if __name__ == "__main__":
    main()
