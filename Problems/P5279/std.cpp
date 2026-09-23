#include <bits/stdc++.h>
using namespace std;

// 返回：长度、左端点（从 1 起）、公共变化量
vector<long long> solve(int n, long long m, const vector<long long>& a) {
  long long best_len = 1, best_l = 1, best_d = 0;
  if (n == 1) {
    vector<long long> one(3);
    one[0] = 1;
    one[1] = 1;
    one[2] = 0;
    return one;
  }
  int i = 0;
  while (i < n - 1) {
    long long d = (a[i + 1] - a[i]) % m;
    if (d < 0) d += m;
    int j = i;
    while (j + 1 < n) {
      long long cur = (a[j + 1] - a[j]) % m;
      if (cur < 0) cur += m;
      if (cur != d) break;
      j++;
    }
    long long cur_len = j - i + 1;
    if (cur_len > best_len) {
      best_len = cur_len;
      best_l = i + 1;
      best_d = d;
    }
    i = j;  // 下一段从当前段末尾接着比
  }
  vector<long long> ans(3);
  ans[0] = best_len;
  ans[1] = best_l;
  ans[2] = best_d;
  return ans;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int n;
  long long m;
  cin >> n >> m;
  vector<long long> a(n);
  for (int i = 0; i < n; i++) cin >> a[i];
  vector<long long> ans = solve(n, m, a);
  cout << ans[0] << " " << ans[1] << " " << ans[2] << "\n";
  return 0;
}
