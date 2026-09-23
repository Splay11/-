#include <bits/stdc++.h>
using namespace std;

int n;                     // 图片数量
int a[1000][1000];        // 相似度矩阵
int fa[1000];             // 并查集的父节点
int ans[1000];            // 每个相似类的相似度之和

// 查找函数，带路径压缩
int find(int x) {
    return x == fa[x] ? x : fa[x] = find(fa[x]);
}

int main() {
    std::ios::sync_with_stdio(false);
    cin >> n;

    // 初始化并查集
    for (int i = 1; i <= n; ++i) {
        fa[i] = i;         // 每个节点的父节点指向自己
    }

    // 读取相似度矩阵并构建并查集
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= n; ++j) {
            cin >> a[i][j];
            if (a[i][j] != 0) {
                int fax = find(i), fay = find(j); // 找到各自的根节点
                if (fax != fay) {
                    fa[fax] = fay;  // 合并两个集合
                }
            }
        }
    }

    // 计算每个相似类的相似度之和
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (a[i][j] && find(i) == find(j)) { // 如果存在相似度并且属于同一类
                ans[find(i)] += a[i][j]; // 将相似度累加到根节点的相似度和中
                a[i][j] = 0;              // 为防止重复计算，将相似度置为0
                a[j][i] = 0;              // 对称位置也置为0
            }
        }
    }
    for(int i = 1; i <= n; i++){
        if(find(i) != i)ans[i] = -1;
    }
    // 输出相似度之和，先排序
    sort(ans + 1, ans + n + 1);
    for (int i = n; i > 0; --i) { // 倒序输出
        if(ans[i] == -1)break;
        cout << ans[i] << " ";
    }

    return 0;
}
