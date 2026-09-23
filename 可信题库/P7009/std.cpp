#include <queue>
#include <vector>
using namespace std;

class Solution {
 public:
  int minTrustDelay(int n, vector<vector<int>>& edges, int src, int dst,
                    int riskBudget) {
    if (src == dst) return 0;
    vector<vector<vector<int>>> g(n);
    for (size_t i = 0; i < edges.size(); i++) {
      vector<int>& e = edges[i];
      g[e[0]].push_back({e[1], e[2], e[3]});
    }
    const long long INF = (1LL << 62);
    vector<vector<long long>> dist(n, vector<long long>(riskBudget + 1, INF));
    dist[src][0] = 0;
    priority_queue<vector<long long>, vector<vector<long long>>, greater<vector<long long>>> pq;
    pq.push({0, (long long)src, 0});
    while (!pq.empty()) {
      vector<long long> cur = pq.top();
      pq.pop();
      long long delay = cur[0];
      int u = (int)cur[1], used = (int)cur[2];
      if (delay != dist[u][used]) continue;
      if (u == dst) return (int)delay;
      for (size_t i = 0; i < g[u].size(); i++) {
        int v = g[u][i][0], w = g[u][i][1], r = g[u][i][2];
        int nu = used + r;
        if (nu > riskBudget) continue;
        long long nd = delay + w;
        if (nd < dist[v][nu]) {
          dist[v][nu] = nd;
          pq.push({nd, (long long)v, (long long)nu});
        }
      }
    }
    return -1;
  }
};
