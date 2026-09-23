#include <iostream>
#include <queue>
#include <vector>
using namespace std;

const long long INF = (long long)4e18;

vector<long long> dijkstra(int p, const vector<vector<pair<int, int> > >& adj, int src) {
    // 从 src 出发的最短公里数
    vector<long long> dist(p + 1, INF);
    dist[src] = 0;
    priority_queue<pair<long long, int>, vector<pair<long long, int> >, greater<pair<long long, int> > > pq;
    pq.push(make_pair(0LL, src));
    while (!pq.empty()) {
        pair<long long, int> cur = pq.top();
        pq.pop();
        long long d = cur.first;
        int u = cur.second;
        if (d != dist[u]) {
            continue;
        }
        for (size_t i = 0; i < adj[u].size(); i++) {
            int v = adj[u][i].first;
            int w = adj[u][i].second;
            long long nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                pq.push(make_pair(nd, v));
            }
        }
    }
    return dist;
}

long long minMeetTime(int p, const vector<vector<int> >& edges, int a, int b,
                      const vector<int>& friends) {
    vector<vector<pair<int, int> > > adj(p + 1);
    for (size_t i = 0; i < edges.size(); i++) {
        int x = edges[i][0], y = edges[i][1], c = edges[i][2], z = edges[i][3];
        adj[x].push_back(make_pair(y, c));
        if (z == 1) {
            adj[y].push_back(make_pair(x, c));
        }
    }
    int q = (int)friends.size();
    vector<vector<long long> > sp(p + 1);
    vector<char> seen(p + 1, 0);
    vector<int> sources;
    sources.push_back(a);
    sources.push_back(b);
    for (int i = 0; i < q; i++) {
        sources.push_back(friends[i]);
    }
    for (size_t i = 0; i < sources.size(); i++) {
        int s = sources[i];
        if (seen[s]) {
            continue;
        }
        seen[s] = 1;
        sp[s] = dijkstra(p, adj, s);
    }
    if (q == 0) {
        return 2 * sp[a][b];
    }
    vector<long long> walk(q);
    for (int i = 0; i < q; i++) {
        walk[i] = 10 * sp[friends[i]][b];
    }
    // dp[mask][i]：已接 mask 里的同伴，当前停在同伴 i 处的最短驾车公里
    int N = 1 << q;
    vector<vector<long long> > dp(N, vector<long long>(q, INF));
    for (int i = 0; i < q; i++) {
        dp[1 << i][i] = sp[a][friends[i]];
    }
    for (int mask = 0; mask < N; mask++) {
        for (int i = 0; i < q; i++) {
            if (dp[mask][i] >= INF) {
                continue;
            }
            if (((mask >> i) & 1) == 0) {
                continue;
            }
            for (int j = 0; j < q; j++) {
                if ((mask >> j) & 1) {
                    continue;
                }
                int nmask = mask | (1 << j);
                long long nd = dp[mask][i] + sp[friends[i]][friends[j]];
                if (nd < dp[nmask][j]) {
                    dp[nmask][j] = nd;
                }
            }
        }
    }
    long long ans = INF;
    for (int mask = 0; mask < N; mask++) {
        long long car;
        if (mask == 0) {
            car = 2 * sp[a][b];
        } else {
            car = INF;
            for (int i = 0; i < q; i++) {
                if ((mask >> i) & 1) {
                    long long cand = 2 * (dp[mask][i] + sp[friends[i]][b]);
                    if (cand < car) {
                        car = cand;
                    }
                }
            }
        }
        long long walkers = 0;
        for (int i = 0; i < q; i++) {
            if (((mask >> i) & 1) == 0) {
                if (walk[i] > walkers) {
                    walkers = walk[i];
                }
            }
        }
        long long cur = car > walkers ? car : walkers;
        if (cur < ans) {
            ans = cur;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int p, e, a, b;
    cin >> p >> e >> a >> b;
    vector<vector<int> > edges(e, vector<int>(4));
    for (int i = 0; i < e; i++) {
        cin >> edges[i][0] >> edges[i][1] >> edges[i][2] >> edges[i][3];
    }
    int q;
    cin >> q;
    vector<int> friends(q);
    for (int i = 0; i < q; i++) {
        cin >> friends[i];
    }
    cout << minMeetTime(p, edges, a, b, friends) << '\n';
    return 0;
}
