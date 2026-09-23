#include <iostream>
using namespace std;

int parent[100005];

// 初始化
void init(int n) {
    for (int i = 1; i <= n; ++i)
        parent[i] = i;
}

// 查找（路径压缩）
int find(int x) {
    if (parent[x] != x)
        parent[x] = find(parent[x]);
    return parent[x];
}

// 合并
void unionSet(int x, int y) {
    int xRoot = find(x);
    int yRoot = find(y);
    if (xRoot != yRoot)
        parent[xRoot] = yRoot;
}

int main() {
    int n, m, z, x, y;
    cin >> n >> m;
    init(n);
    for (int i = 0; i < m; i++) {
        cin >> z >> x >> y;
        if (z == 1) {
            unionSet(x, y);
        } else {
            if (find(x) == find(y))
                cout << "Y\n";
            else
                cout << "N\n";
        }
    }
    return 0;
}
