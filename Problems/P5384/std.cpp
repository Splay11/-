#include <array>
#include <iostream>
#include <queue>
#include <tuple>
#include <vector>
using namespace std;

const long long INF = (1LL << 62);

struct Road {
    int u, v;
    long long d;
};

struct Edge {
    int to;
    long long w;
    Edge(int to, long long w) : to(to), w(w) {}
};

// 状态最短路：工位 u、已用罐笼 used、上一步是否罐笼 last
long long min_time(int n, const vector<Road>& roads,
                   const vector<pair<int, int> >& portals,
                   int cap, int src, int dst) {
    if (src == dst) {
        return 0;
    }
    vector<vector<Edge> > g(n);
    for (size_t i = 0; i < roads.size(); i++) {
        int u = roads[i].u, v = roads[i].v;
        long long d = roads[i].d;
        g[u].push_back(Edge(v, d));
        g[v].push_back(Edge(u, d));
    }
    vector<vector<int> > pg(n);
    for (size_t i = 0; i < portals.size(); i++) {
        int u = portals[i].first, v = portals[i].second;
        pg[u].push_back(v);
        pg[v].push_back(u);
    }
    vector<vector<array<long long, 2> > > dist(
        n, vector<array<long long, 2> >(cap + 1));
    for (int i = 0; i < n; i++) {
        for (int used = 0; used <= cap; used++) {
            dist[i][used][0] = INF;
            dist[i][used][1] = INF;
        }
    }
    dist[src][0][0] = 0;
    typedef tuple<long long, int, int, int> State;
    priority_queue<State, vector<State>, greater<State> > pq;
    pq.push(State(0, src, 0, 0));
    while (!pq.empty()) {
        long long cur;
        int u, used, last;
        tie(cur, u, used, last) = pq.top();
        pq.pop();
        if (cur != dist[u][used][last]) {
            continue;
        }
        if (u == dst) {
            return cur;
        }
        // 普通巷道：次数不变，last 置 0
        for (size_t i = 0; i < g[u].size(); i++) {
            int v = g[u][i].to;
            long long nd = cur + g[u][i].w;
            if (nd < dist[v][used][0]) {
                dist[v][used][0] = nd;
                pq.push(State(nd, v, used, 0));
            }
        }
        // 罐笼：不能连坐，且次数未用尽；出发时可直接坐
        if (last == 0 && used < cap) {
            for (size_t i = 0; i < pg[u].size(); i++) {
                int v = pg[u][i];
                if (cur < dist[v][used + 1][1]) {
                    dist[v][used + 1][1] = cur;
                    pq.push(State(cur, v, used + 1, 1));
                }
            }
        }
    }
    return -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<Road> roads(m);
    for (int i = 0; i < m; i++) {
        cin >> roads[i].u >> roads[i].v >> roads[i].d;
    }
    int p;
    cin >> p;
    vector<pair<int, int> > portals(p);
    for (int i = 0; i < p; i++) {
        cin >> portals[i].first >> portals[i].second;
    }
    int cap, src, dst;
    cin >> cap >> src >> dst;
    cout << min_time(n, roads, portals, cap, src, dst) << '\n';
    return 0;
}
