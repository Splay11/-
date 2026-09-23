#include <bits/stdc++.h>
using namespace std;

struct Solver {
  int n;
  vector<int> parent, sgn;
  vector<long long> off, fixedv;
  vector<char> has;

  Solver(int n_) : n(n_) {
    parent.resize(n + 1);
    sgn.assign(n + 1, 1);
    off.assign(n + 1, 0);
    fixedv.assign(n + 1, 0);
    has.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) parent[i] = i;
  }

  // 迭代路径压缩，同时把一次式接到根上
  // c[x] = sgn[x] * c[root] + off[x]
  int find(int x) {
    vector<int> path;
    while (parent[x] != x) {
      path.push_back(x);
      x = parent[x];
    }
    int r = x;
    for (int i = (int)path.size() - 1; i >= 0; i--) {
      int v = path[i];
      int p = parent[v];
      int os = sgn[v];
      sgn[v] = os * sgn[p];
      off[v] = off[v] + 1LL * os * off[p];
      parent[v] = r;
    }
    return r;
  }

  // 加入方程 c[a] + ka * c[b] = val；D 时 ka=-1，S 时 ka=1
  bool add(int a, int b, int ka, long long val) {
    int ra = find(a), rb = find(b);
    int sa = sgn[a], sb = sgn[b];
    long long oa = off[a], ob = off[b];
    long long rhs = val - oa - 1LL * ka * ob;
    if (ra == rb) {
      int coef = sa + ka * sb;
      if (coef == 0) return rhs == 0;  // 冗余或矛盾
      if (rhs % coef != 0) return false;  // 根不是整数
      long long need = rhs / coef;
      if (has[ra] && fixedv[ra] != need) return false;
      has[ra] = 1;
      fixedv[ra] = need;
      return true;
    }
    // 把 ra 挂到 rb
    parent[ra] = rb;
    sgn[ra] = -sa * ka * sb;
    off[ra] = sa * rhs;
    if (has[ra] && has[rb]) return fixedv[ra] == sgn[ra] * fixedv[rb] + off[ra];
    if (has[ra]) {
      // 已知 rA，反推 rB
      has[rb] = 1;
      fixedv[rb] = sgn[ra] * (fixedv[ra] - off[ra]);
    }
    return true;
  }

  pair<string, long long> run(const vector<tuple<char, int, int, long long> >& cons) {
    for (size_t i = 0; i < cons.size(); i++) {
      char typ = get<0>(cons[i]);
      int a = get<1>(cons[i]), b = get<2>(cons[i]);
      long long w = get<3>(cons[i]);
      bool ok = (typ == 'D') ? add(a, b, -1, w) : add(a, b, 1, w);
      if (!ok) return make_pair(string("NO"), -1LL);
    }
    vector<char> seen(n + 1, 0);
    long long k = 0;
    for (int i = 1; i <= n; i++) {
      int r = find(i);
      if (!seen[r]) {
        seen[r] = 1;
        if (!has[r]) k++;  // 未钉死的根各贡献一个自由度
      }
    }
    return make_pair(string("YES"), k);
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<tuple<char, int, int, long long> > cons;
  for (int i = 0; i < m; i++) {
    char typ;
    int a, b;
    long long w;
    cin >> typ >> a >> b >> w;
    cons.push_back(make_tuple(typ, a, b, w));
  }
  pair<string, long long> ans = Solver(n).run(cons);
  cout << ans.first << "\n" << ans.second << "\n";
  return 0;
}
