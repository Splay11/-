# 并查集类定义
class UnionFind:
    def __init__(self, n):
        self.fa = list(range(n + 1))  # 初始化父节点

    def find(self, x):
        if x != self.fa[x]:
            self.fa[x] = self.find(self.fa[x])  # 路径压缩
        return self.fa[x]

def main():
    n = int(input().strip())  # 读取图片数量
    a = [list(map(int, input().strip().split())) for _ in range(n)]  # 读取相似度矩阵
    uf = UnionFind(n)  # 创建并查集实例
    ans = [0] * (n + 1)  # 每个相似类的相似度之和

    # 读取相似度矩阵并构建并查集
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if a[i - 1][j - 1] != 0:  # 注意索引从0开始
                fax = uf.find(i)  # 找到第i个图片的根节点
                fay = uf.find(j)  # 找到第j个图片的根节点
                if fax != fay:
                    uf.fa[fax] = fay  # 合并两个集合

    # 计算每个相似类的相似度之和
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if a[i - 1][j - 1] != 0 and uf.find(i) == uf.find(j):
                ans[uf.find(i)] += a[i - 1][j - 1]  # 将相似度累加到根节点的相似度和中
                a[i - 1][j - 1] = 0  # 为防止重复计算，将相似度置为0
                a[j - 1][i - 1] = 0  # 对称位置也置为0
    for i in range(1,n+1):
        if uf.find(i) != i:
            ans[i] = -1
    # 输出相似度之和，先排序
    sorted_ans = sorted(ans[1:], reverse=True)  # 排序并去掉第0个元素
    for score in sorted_ans:
        if score == -1:
            break
        print(score, end=' ')  # 打印相似度和

if __name__ == "__main__":
    main()
