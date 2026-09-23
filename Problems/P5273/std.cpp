#include <bits/stdc++.h>
using namespace std;

bool can(int limit, const vector<int>& dur, int days, int help_k) {
  // 判断主责单日上限为 limit 时，能否在 days 天内按顺序做完
  int n = (int)dur.size();
  int i = 0, used = 0;
  while (i < n) {
    used++;
    if (used > days) return false;
    // dp[t] 第 s 位：当天已交接 t 卷、支援耗时恰好为 s
    vector<bitset<481> > dp(help_k + 1), ndp(help_k + 1);
    dp[0].set(0);
    int total = 0;
    int last = i - 1;
    for (int j = i; j < n; j++) {
      int x = dur[j];
      total += x;
      for (int t = 0; t <= help_k; t++) ndp[t].reset();
      if (x <= limit) {
        // 主责可做：留给自己，或交给支援
        for (int t = 0; t <= help_k; t++) {
          ndp[t] = dp[t];
          if (t > 0) ndp[t] |= (dp[t - 1] << x);
        }
      } else {
        // 必须交给支援
        for (int t = 1; t <= help_k; t++) ndp[t] = dp[t - 1] << x;
      }
      int need = total - limit;
      if (need < 0) need = 0;
      bool ok = false;
      for (int t = 0; t <= help_k; t++) {
        if ((ndp[t] >> need).any()) {
          ok = true;
          break;
        }
      }
      if (!ok) break;
      dp.swap(ndp);
      last = j;
    }
    if (last < i) return false;
    i = last + 1;
  }
  return true;
}

int solve(int n, int m, int k, const vector<int>& dur) {
  (void)n;
  // 主责每天也最多 480，先看有没有解
  if (!can(480, dur, m, k)) return -1;
  int lo = 0, hi = 480;
  while (lo < hi) {
    int mid = (lo + hi) / 2;
    if (can(mid, dur, m, k)) hi = mid;
    else lo = mid + 1;
  }
  return lo;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int n, m, k;
  cin >> n >> m >> k;
  vector<int> dur(n);
  for (int i = 0; i < n; i++) cin >> dur[i];
  cout << solve(n, m, k, dur) << "\n";
  return 0;
}
