def parse_lists(s):
    s = s.strip()
    inner = s[1:-1]
    lists = []
    i = 0
    n = len(inner)
    while i < n:
        if inner[i] == ",":
            i += 1
            continue
        j = i + 1
        while j < n and inner[j] != "}":
            j += 1
        body = inner[i + 1 : j]
        if body == "":
            lists.append([])
        else:
            lists.append([int(x) for x in body.split(",")])
        i = j + 1
    return lists


def merge_rev(lists):
    out = []
    for i in range(len(lists) - 1, -1, -1):
        out.extend(lists[i])
    return out


def format_list(vals):
    if not vals:
        return "{}"
    return "{" + ",".join(str(x) for x in vals) + "}"


if __name__ == "__main__":
    line = input()
    print(format_list(merge_rev(parse_lists(line))))
