#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> p, r;
    DSU(int n = 0) { init(n); }
    void init(int n) { p.resize(n+1); r.assign(n+1, 0); iota(p.begin(), p.end(), 0); }
    int find(int x){ return p[x]==x?x:p[x]=find(p[x]); }
    bool unite(int a, int b){
        a = find(a); b = find(b);
        if(a == b) return false;
        if(r[a] < r[b]) swap(a, b);
        p[b] = a;
        if(r[a] == r[b]) r[a]++;
        return true;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T; 
    if(!(cin >> T)) return 0;
    while (T--) {
        int n, m; 
        cin >> n >> m;

        // 读入“不同”对：输入分两行给出 m 个 x 和 m 个 y
        vector<int> X(m), Y(m);
        for (int i = 0; i < m; ++i) cin >> X[i];
        for (int i = 0; i < m; ++i) cin >> Y[i];

        // 用布尔矩阵标记不同
        vector<vector<char>> diff(n+1, vector<char>(n+1, 0));
        for (int i = 0; i < m; ++i) {
            int x = X[i], y = Y[i];
            diff[x][y] = diff[y][x] = 1; // 标记两者不同
        }

        DSU dsu(n);
        // 枚举补图（即未标为不同的对）做并查集合并，表示“相同”
        for (int i = 1; i <= n; ++i) {
            for (int j = i+1; j <= n; ++j) {
                if (!diff[i][j]) { // 未被标记为不同 => 认为相同
                    dsu.unite(i, j);
                }
            }
        }

        // 检查：任一“不同”对是否被并到了同一集合
        bool ok = true;
        for (int i = 0; i < m && ok; ++i) {
            if (dsu.find(X[i]) == dsu.find(Y[i])) {
                ok = false;
            }
        }
        cout << (ok ? "Yes" : "No") << "\n";
    }
    return 0;
}
