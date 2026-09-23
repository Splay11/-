#include <iostream>
#include <vector>
#include <queue>
#include <utility>
using namespace std;

int max_bottleneck(int c, int t, const vector<vector<int>>& edges) {
    vector<vector<pair<int, int>>> graph(c);
    for (size_t i = 0; i < edges.size(); i++) {
        int x = edges[i][0], y = edges[i][1], b = edges[i][2];
        graph[x].push_back(make_pair(y, b));
        graph[y].push_back(make_pair(x, b));
    }
    const int INF = 1000000000;
    // f[u][used]：到达 u、恰好升级 used 次时，能得到的最大瓶颈
    vector<vector<int>> f(c, vector<int>(t + 1, -1));
    f[0][0] = INF;
    priority_queue<pair<int, pair<int, int>>> pq;
    pq.push(make_pair(INF, make_pair(0, 0)));
    while (!pq.empty()) {
        int bneck = pq.top().first;
        int u = pq.top().second.first;
        int used = pq.top().second.second;
        pq.pop();
        if (bneck < f[u][used]) {
            continue;
        }
        for (size_t i = 0; i < graph[u].size(); i++) {
            int v = graph[u][i].first;
            int w = graph[u][i].second;
            // 不升级这条边
            int nxt0 = (bneck == INF) ? w : min(bneck, w);
            if (nxt0 > f[v][used]) {
                f[v][used] = nxt0;
                pq.push(make_pair(nxt0, make_pair(v, used)));
            }
            // 升级这条边，带宽变为 2w
            if (used < t) {
                int ww = 2 * w;
                int nxt1 = (bneck == INF) ? ww : min(bneck, ww);
                if (nxt1 > f[v][used + 1]) {
                    f[v][used + 1] = nxt1;
                    pq.push(make_pair(nxt1, make_pair(v, used + 1)));
                }
            }
        }
    }
    int ans = f[c - 1][0];
    if (t > 0) {
        ans = max(ans, f[c - 1][t]);
    }
    if (ans < 0) {
        return -1;
    }
    return ans;
}

int main() {
    int c, d, t;
    cin >> c >> d >> t;
    vector<vector<int>> edges;
    for (int i = 0; i < d; i++) {
        int x, y, b;
        cin >> x >> y >> b;
        vector<int> e;
        e.push_back(x);
        e.push_back(y);
        e.push_back(b);
        edges.push_back(e);
    }
    cout << max_bottleneck(c, t, edges) << endl;
    return 0;
}
