// 思路同上：线路做点、同站相交的线路连边，查询时在线路图上 BFS。
#include <bits/stdc++.h>
using namespace std;

// 求一次查询的最少换乘
int bfs_min_transfers(int s, int t,
                      const vector<vector<int>>& stationLines,
                      const vector<vector<int>>& adj) {
    if (s == t) return 0;
    const vector<int>& starts = stationLines[s];
    const vector<int>& tlist  = stationLines[t];
    if (starts.empty() || tlist.empty()) return -1;

    int m = (int)adj.size();
    vector<char> isTarget(m, 0);
    for (int x : tlist) isTarget[x] = 1;
    for (int x : starts) if (isTarget[x]) return 0;

    vector<int> dist(m, -1);
    queue<int> q;
    for (int x : starts) { dist[x] = 0; q.push(x); }

    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                if (isTarget[v]) return dist[v];
                q.push(v);
            }
        }
    }
    return -1; // 不可达
}

// 构建站点->线路与线路图
void build_graph(int n, int m, const vector<vector<int>>& lines,
                 vector<vector<int>>& stationLines,
                 vector<vector<int>>& adj) {
    for (int i = 0; i < m; ++i) {
        for (int s : lines[i]) {
            stationLines[s].push_back(i);
        }
    }
    for (int s = 0; s < n; ++s) {
        const auto& lst = stationLines[s];
        for (int i = 0; i < (int)lst.size(); ++i) {
            int a = lst[i];
            for (int j = i + 1; j < (int)lst.size(); ++j) {
                int b = lst[j];
                adj[a].push_back(b);
                adj[b].push_back(a);
            }
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, k;
    if (!(cin >> n >> m >> k)) return 0;

    vector<vector<int>> lines(m);
    for (int i = 0; i < m; ++i) {
        int cnt; cin >> cnt;
        lines[i].resize(cnt);
        for (int j = 0; j < cnt; ++j) cin >> lines[i][j];
    }

    vector<vector<int>> stationLines(n);
    vector<vector<int>> adj(m);
    build_graph(n, m, lines, stationLines, adj);

    for (int i = 0; i < k; ++i) {
        int s, t; cin >> s >> t;
        cout << bfs_min_transfers(s, t, stationLines, adj) << "\n";
    }
    return 0;
}
