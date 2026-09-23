#include <iostream>
#include <vector>
#include <cstdlib>
using namespace std;

const int INF = 1000000000;
const int MAXK = 16;

// 把非 0 格子当成城市，用状压 DP 求从中心出发并返回的最短回路
int min_steps(const vector<vector<int>>& grid) {
    int n = (int)grid.size();
    int m = (int)grid[0].size();
    int sr = n / 2, sc = m / 2;
    // 点 0 固定为中心，其余点为中心以外的非 0 格子
    vector<pair<int, int>> pts;
    pts.push_back({sr, sc});
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (grid[i][j] != 0 && (i != sr || j != sc)) {
                pts.push_back({i, j});
            }
        }
    }
    int k = (int)pts.size();
    if (k == 1) {
        return 0;
    }
    int dist[MAXK][MAXK];
    for (int a = 0; a < k; a++) {
        for (int b = 0; b < k; b++) {
            dist[a][b] = abs(pts[a].first - pts[b].first) + abs(pts[a].second - pts[b].second);
        }
    }
    int full = 1 << k;
    // dp[mask][i]：已访问集合为 mask、当前停在 i 的最少步数
    vector<vector<int>> dp(full, vector<int>(k, INF));
    dp[1][0] = 0;
    for (int mask = 0; mask < full; mask++) {
        for (int i = 0; i < k; i++) {
            if (((mask >> i) & 1) == 0 || dp[mask][i] >= INF) {
                continue;
            }
            for (int j = 0; j < k; j++) {
                if ((mask >> j) & 1) {
                    continue;
                }
                int nxt = mask | (1 << j);
                int cand = dp[mask][i] + dist[i][j];
                if (cand < dp[nxt][j]) {
                    dp[nxt][j] = cand;
                }
            }
        }
    }
    int end = full - 1;
    int ans = INF;
    // 访问完全部点后，还要走回中心
    for (int i = 0; i < k; i++) {
        int cand = dp[end][i] + dist[i][0];
        if (cand < ans) {
            ans = cand;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> grid(n, vector<int>(m));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> grid[i][j];
        }
    }
    cout << min_steps(grid) << "\n";
    return 0;
}
