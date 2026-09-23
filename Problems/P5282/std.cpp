#include <bits/stdc++.h>
using namespace std;

using ll = long long;

bool max_sum_len_ge(const vector<ll>& a, int L, ll& out) {
  int n = (int)a.size();
  if (n < L) return false;
  vector<ll> P(n + 1, 0);
  for (int i = 0; i < n; i++) P[i + 1] = P[i] + a[i];
  ll best = P[L] - P[0];
  ll mn = P[0];
  for (int r = L; r <= n; r++) {
    best = max(best, P[r] - mn);
    int nxt = r - L + 1;
    if (nxt <= n && P[nxt] < mn) mn = P[nxt];
  }
  out = best;
  return true;
}

int main() {
  int n, m;
  cin >> n >> m;
  vector<vector<int>> g(n, vector<int>(m));
  for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++) cin >> g[i][j];

  ll ans = LLONG_MIN / 4;
  for (int top = 0; top < n; top++) {
    vector<ll> col(m, 0);
    for (int bottom = top; bottom < n; bottom++) {
      int h = bottom - top + 1;
      for (int j = 0; j < m; j++) col[j] += g[bottom][j];
      ll s;
      if (max_sum_len_ge(col, h, s)) ans = max(ans, (ll)h * s);
    }
  }
  for (int left = 0; left < m; left++) {
    vector<ll> row(n, 0);
    for (int right = left; right < m; right++) {
      int w = right - left + 1;
      for (int i = 0; i < n; i++) row[i] += g[i][right];
      ll s;
      if (max_sum_len_ge(row, w, s)) ans = max(ans, (ll)w * s);
    }
  }
  cout << ans << "\n";
  return 0;
}
