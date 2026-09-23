#include <bits/stdc++.h>
using namespace std;

double solve(int n, const vector<int>& fa, const vector<int>& w, int W) {
  // 建二叉树：每个点最多两个孩子。保证 fa[i]<i，孩子编号更大
  vector<vector<int> > ch(n);
  for (int i = 1; i < n; i++) ch[fa[i - 1]].push_back(i);

  vector<int> sz(n, 1);
  vector<double> sumw(n, 0), edfn(n, 0);
  // 编号递增保证孩子更大，倒序就是自底向上
  for (int u = n - 1; u >= 0; u--) {
    double sw = w[u];
    int s = 1;
    for (size_t k = 0; k < ch[u].size(); k++) {
      int v = ch[u][k];
      s += sz[v];
      sw += sumw[v];
    }
    sz[u] = s;
    sumw[u] = sw;
  }

  // 根的 DFS 序恒为 1，再往下推每个孩子的期望序
  edfn[0] = 1.0;
  vector<int> st;
  st.push_back(0);
  while (!st.empty()) {
    int u = st.back();
    st.pop_back();
    if (ch[u].empty()) continue;
    if (ch[u].size() == 1) {
      // 独子：下一个被访问的一定是它
      int v = ch[u][0];
      edfn[v] = edfn[u] + 1.0;
      st.push_back(v);
      continue;
    }
    int a = ch[u][0], b = ch[u][1];
    double wa = w[a], wb = w[b], s = wa + wb;
    // 先走兄弟整棵子树，会把对方子树大小加进自己的期望序
    edfn[a] = edfn[u] + 1.0 + (wb / s) * sz[b];
    edfn[b] = edfn[u] + 1.0 + (wa / s) * sz[a];
    st.push_back(a);
    st.push_back(b);
  }

  double base = 0;
  for (int i = 0; i < n; i++) base += w[i] * (n + 1.0 - edfn[i]);
  double best = base;

  // 枚举把某一个点改成 W；不改的情况已经在 base 里
  for (int x = 0; x < n; x++) {
    if (w[x] == W) continue;
    double extra = (W - w[x]) * (n + 1.0 - edfn[x]);
    int p = (x > 0) ? fa[x - 1] : -1;
    int sib = -1;
    if (p >= 0 && (int)ch[p].size() == 2) {
      sib = (ch[p][0] == x) ? ch[p][1] : ch[p][0];
    }
    if (sib >= 0) {
      // 改的是双孩子中的一侧，兄弟先后概率跟着变
      double wx = w[x], ws = w[sib];
      double old_den = wx + ws, new_den = W + ws;
      double d_x = (ws / new_den - ws / old_den) * sz[sib];
      double d_s = ((double)W / new_den - wx / old_den) * sz[x];
      extra -= d_x * (sumw[x] - w[x] + W);
      extra -= d_s * sumw[sib];
    }
    best = max(best, base + extra);
  }
  return best;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  // 点数、n-1 个父亲、n 个权值、目标权值
  int n;
  cin >> n;
  vector<int> fa(max(0, n - 1));
  for (int i = 0; i < n - 1; i++) cin >> fa[i];
  vector<int> w(n);
  for (int i = 0; i < n; i++) cin >> w[i];
  int W;
  cin >> W;
  cout << fixed << setprecision(4) << solve(n, fa, w, W) << "\n";
  return 0;
}
