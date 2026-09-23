import json
from itertools import combinations


def support_of(itemset, recs):
    s = set(itemset)
    return sum(1 for r in recs if s <= r)


def frequent_itemsets(records, min_cnt):
    recs = [set(r) for r in records]
    cnt = {}
    for r in recs:
        for x in r:
            cnt[x] = cnt.get(x, 0) + 1
    G = sorted((x,) for x, c in cnt.items() if c >= min_cnt)
    U = []
    while G:
        G_set = set(G)
        k = len(G[0])
        for itemset in G:
            U.append([list(itemset), support_of(itemset, recs)])
        D = []
        for i in range(len(G)):
            for j in range(i + 1, len(G)):
                a, b = G[i], G[j]
                if a[:-1] == b[:-1] and a[-1] < b[-1]:
                    cand = a + (b[-1],)
                    ok = True
                    for sub in combinations(cand, k):
                        if sub not in G_set:
                            ok = False
                            break
                    if ok:
                        D.append(cand)
        G = []
        for cand in D:
            if support_of(cand, recs) >= min_cnt:
                G.append(cand)
        G.sort()
    U.sort(key=lambda x: (len(x[0]), x[0]))
    return U


def read_json():
    chunks = []
    while True:
        try:
            chunks.append(input())
        except EOFError:
            break
    return json.loads("\n".join(chunks))


def main():
    data = read_json()
    ans = frequent_itemsets(data["records"], data["min_cnt"])
    print(json.dumps(ans))


if __name__ == "__main__":
    main()
