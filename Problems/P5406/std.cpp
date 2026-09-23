// 从入口、出口各跑一次 Dijkstra，再枚举哪条通道免费
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

const long long INF = (1LL << 62);

vector<long long> dijkstra(int n, int src, const vector<vector<pair<int, int> > >& adj) {
    vector<long long> dist(n + 1, INF);
    dist[src] = 0;
    priority_queue<pair<long long, int>, vector<pair<long long, int> >, greater<pair<long long, int> > > heap;
    heap.push(make_pair(0LL, src));
    while (!heap.empty()) {
        long long d = heap.top().first;
        int u = heap.top().second;
        heap.pop();
        if (d != dist[u]) {
            continue;
        }
        for (size_t i = 0; i < adj[u].size(); i++) {
            int v = adj[u][i].first;
            int w = adj[u][i].second;
            long long nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                heap.push(make_pair(nd, v));
            }
        }
    }
    return dist;
}

long long minWithOneFree(int n, int s, int t, const vector<vector<int> >& edges,
                         const vector<vector<pair<int, int> > >& adj) {
    // 入口即出口，不必移动
    if (s == t) {
        return 0;
    }
    vector<long long> ds = dijkstra(n, s, adj);
    vector<long long> dt = dijkstra(n, t, adj);
    long long ans = ds[t];
    for (size_t i = 0; i < edges.size(); i++) {
        int u = edges[i][0];
        int v = edges[i][1];
        // 免费走 u -> v
        if (ds[u] < INF / 2 && dt[v] < INF / 2) {
            long long nd = ds[u] + dt[v];
            if (nd < ans) {
                ans = nd;
            }
        }
        // 通道是双向的，另一方向同样可以免费
        if (ds[v] < INF / 2 && dt[u] < INF / 2) {
            long long nd = ds[v] + dt[u];
            if (nd < ans) {
                ans = nd;
            }
        }
    }
    return ans >= INF / 2 ? -1 : ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    vector<vector<int> > edges;
    vector<vector<pair<int, int> > > adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        vector<int> e;
        e.push_back(u);
        e.push_back(v);
        e.push_back(w);
        edges.push_back(e);
        adj[u].push_back(make_pair(v, w));
        adj[v].push_back(make_pair(u, w));
    }
    cout << minWithOneFree(n, s, t, edges, adj) << "\n";
    return 0;
}
