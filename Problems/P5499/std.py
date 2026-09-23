def normalize(part):
    # 去掉前导零；全零则保留单个 0
    i = 0
    while i < len(part) - 1 and part[i] == '0':
        i += 1
    return part[i:]


def compare_part(a, b):
    # 不能转整数：修订号可能超过 64 位；先比长度再比字典序
    if len(a) != len(b):
        return 1 if len(a) > len(b) else -1
    if a != b:
        return 1 if a > b else -1
    return 0


def compare_version(v1, v2):
    p1 = [normalize(x) for x in v1.split('.')]
    p2 = [normalize(x) for x in v2.split('.')]
    n = max(len(p1), len(p2))
    for i in range(n):
        a = p1[i] if i < len(p1) else '0'
        b = p2[i] if i < len(p2) else '0'
        c = compare_part(a, b)
        if c != 0:
            return c
    return 0


def main():
    v1 = input().strip()
    v2 = input().strip()
    print(compare_version(v1, v2))


if __name__ == "__main__":
    main()
