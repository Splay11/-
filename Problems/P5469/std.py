# 按当前波次的标签增量贪心挑主机；增量打平时取更小的 nid


def assign_batches(hosts, dim_cnt, batch_cnt):
    """
    hosts: [(nid, [tag_1, ..., tag_d]), ...]
    按题面规则把主机分进 batch_cnt 个波次。
    返回每个波次内已按 nid 升序排好的列表。
    """
    total = len(hosts)
    # 前 (b-r) 波容量 q，最后 r 波容量 q+1
    base = total // batch_cnt
    extra = total % batch_cnt
    sizes = [base] * (batch_cnt - extra) + [base + 1] * extra

    used = set()
    result = []
    for cap in sizes:
        wave = []
        # 每个维度各自维护「本波次已出现过的标签」
        seen = [set() for _ in range(dim_cnt)]
        for _ in range(cap):
            best_inc = -1
            best_nid = None
            best_tags = None
            for nid, tags in hosts:
                if nid in used:
                    continue
                # 增量：该机各维标签里，本波次还没出现过的个数
                inc = 0
                for j in range(dim_cnt):
                    if tags[j] not in seen[j]:
                        inc += 1
                # 增量更大优先；打平则 nid 更小优先
                if inc > best_inc or (inc == best_inc and (best_nid is None or nid < best_nid)):
                    best_inc = inc
                    best_nid = nid
                    best_tags = tags
            used.add(best_nid)
            wave.append(best_nid)
            for j in range(dim_cnt):
                seen[j].add(best_tags[j])
        wave.sort()
        result.append(wave)
    return result


def main():
    p, d = map(int, input().split())
    hosts = []
    for _ in range(p):
        parts = input().split()
        nid = int(parts[0])
        tags = parts[1:]
        hosts.append((nid, tags))
    b = int(input())
    waves = assign_batches(hosts, d, b)
    for wave in waves:
        print(" ".join(str(x) for x in wave))


if __name__ == "__main__":
    main()
