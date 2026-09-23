#include <functional>
#include <iostream>
#include <vector>
using namespace std;

// 在 1-边构成的二分图上求最大匹配；得分 = 2*匹配 - m
int max_matching(const vector<vector<int>> &g) {
    int m = (int)g.size();
    vector<int> match_r(m, -1);

    function<bool(int, vector<char> &)> dfs = [&](int u, vector<char> &seen) -> bool {
        // 从我方 u 出发找增广路
        for (int v = 0; v < m; v++) {
            if (g[u][v] == 1 && !seen[v]) {
                seen[v] = 1;
                if (match_r[v] == -1 || dfs(match_r[v], seen)) {
                    match_r[v] = u;
                    return true;
                }
            }
        }
        return false;
    };

    int cnt = 0;
    for (int u = 0; u < m; u++) {
        vector<char> seen(m, 0);
        if (dfs(u, seen)) {
            cnt++;
        }
    }
    return cnt;
}

int best_score(const vector<vector<int>> &g) {
    int m = (int)g.size();
    return 2 * max_matching(g) - m;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        vector<vector<int>> g(m, vector<int>(m));
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                cin >> g[i][j];
            }
        }
        cout << best_score(g) << "\n";
    }
    return 0;
}
