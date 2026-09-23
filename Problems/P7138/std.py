class Node:
    def __init__(self):
        # 字典树节点：儿子边、是否有词根在此结束
        self.ch = {}
        self.end = False


def insert(root, word):
    """把一个词根插入字典树。"""
    cur = root
    for c in word:
        if c not in cur.ch:
            cur.ch[c] = Node()
        cur = cur.ch[c]
    cur.end = True


def shortest_root(root, word):
    """沿单词往下走，第一次碰到词根结束标记，就是最短词根。
    走不通或走完都没有结束标记，则整词保留。
    """
    cur = root
    for i, c in enumerate(word):
        if c not in cur.ch:
            return word
        cur = cur.ch[c]
        if cur.end:
            return word[: i + 1]
    return word


def solve(dictionary, sentence):
    root = Node()
    for w in dictionary:
        insert(root, w)
    words = sentence.split(" ")
    out = []
    for w in words:
        out.append(shortest_root(root, w))
    return " ".join(out)


def main():
    # 第一行：词根个数 n
    n = int(input())
    # 第二行：n 个词根
    dictionary = input().split()
    # 第三行：整句，单词之间恰好一个空格
    sentence = input()
    print(solve(dictionary, sentence))


if __name__ == "__main__":
    main()
