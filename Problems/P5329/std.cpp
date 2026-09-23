#include <iostream>
#include <queue>
#include <vector>
using namespace std;

struct E {
  int v, c, t;
};

struct St {
  long long tm;
  int u, f;
  bool operator<(const St &o) const { return tm > o.tm; }
};

long long solve(int k, int q, vector<int> r, vector<vector<E> > g) {
  const long long inf = 1000000000000000000LL;
  vector<vector<long long> > dist(k + 1, vector<long long>(q + 1, inf));
  dist[1][q] = 0;
  priority_queue<St> pq;
  pq.push((St){0, 1, q});
  while (!pq.empty()) {
    St cur = pq.top();
    pq.pop();
    if (cur.tm != dist[cur.u][cur.f]) continue;
    if (cur.f < q) {
      long long ntm = cur.tm + r[cur.u - 1];
      int nf = cur.f + 1;
      if (ntm < dist[cur.u][nf]) {
        dist[cur.u][nf] = ntm;
        pq.push((St){ntm, cur.u, nf});
      }
    }
    for (int i = 0; i < (int)g[cur.u].size(); i++) {
      E e = g[cur.u][i];
      if (cur.f >= e.c) {
        long long ntm = cur.tm + e.t;
        int nf = cur.f - e.c;
        if (ntm < dist[e.v][nf]) {
          dist[e.v][nf] = ntm;
          pq.push((St){ntm, e.v, nf});
        }
      }
    }
  }
  long long ans = inf;
  for (int f = 0; f <= q; f++) if (dist[k][f] < ans) ans = dist[k][f];
  if (ans >= inf) return -1;
  return ans;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int k, e, q;
  cin >> k >> e >> q;
  vector<int> r(k);
  for (int i = 0; i < k; i++) cin >> r[i];
  vector<vector<E> > g(k + 1);
  for (int i = 0; i < e; i++) {
    int a, b, c, t;
    cin >> a >> b >> c >> t;
    g[a].push_back((E){b, c, t});
    g[b].push_back((E){a, c, t});
  }
  cout << solve(k, q, r, g) << "\n";
  return 0;
}
