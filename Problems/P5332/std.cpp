#include <iostream>
#include <vector>
using namespace std;

const long long INF = (long long)1e18;

long long solve(int k, int q, int w, const vector<int> &v) {
  // 每个位置只补 0..q-1；链上后面的格由模关系唯一确定
  if (w == 1) {
    long long ans = 0;
    for (int i = 0; i < k; i++) ans += (q - v[i] % q) % q;
    return ans;
  }
  vector<int> pref(k + 1);
  for (int i = 0; i < k; i++) pref[i + 1] = pref[i] + v[i];
  int nwin = k - w + 1;
  vector<int> s(nwin);
  for (int p = 0; p < nwin; p++) s[p] = ((pref[p + w] - pref[p]) % q + q) % q;
  int need = ((-s[0]) % q + q) % q;
  if (w == k) return need;

  vector<vector<long long> > chain(w, vector<long long>(q));
  for (int r = 0; r < w; r++) {
    for (int x = 0; x < q; x++) {
      long long cost = x;
      int cur = x;
      int p = r;
      while (p + w < k) {
        cur = (cur + s[p] - s[p + 1]) % q;
        if (cur < 0) cur += q;
        cost += cur;
        p += w;
      }
      chain[r][x] = cost;
    }
  }

  vector<long long> dp(q, INF);
  dp[0] = 0;
  for (int r = 0; r < w; r++) {
    vector<long long> ndp(q, INF);
    for (int md = 0; md < q; md++) {
      if (dp[md] >= INF) continue;
      for (int x = 0; x < q; x++) {
        int j = md + x;
        if (j >= q) j -= q;
        long long val = dp[md] + chain[r][x];
        if (val < ndp[j]) ndp[j] = val;
      }
    }
    dp.swap(ndp);
  }
  return dp[need];
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int k, q, w;
  cin >> k >> q >> w;
  vector<int> v(k);
  for (int i = 0; i < k; i++) cin >> v[i];
  cout << solve(k, q, w, v) << "\n";
  return 0;
}
