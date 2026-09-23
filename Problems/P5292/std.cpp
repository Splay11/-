#include <bits/stdc++.h>
using namespace std;

bool can_reach(int n, const vector<long long>& a, long long m, int k, long long x) {
  // 差分数组记录区间加何时失效
  vector<long long> diff(n + 1, 0);
  long long add = 0, used = 0;
  for (int i = 0; i < n; i++) {
    add += diff[i];
    long long need = x - a[i] - add;
    if (need > 0) {
      used += need;
      if (used > m) return false;
      // 左端钉在 i，窗口尽量长为 k
      add += need;
      long long end = i + 1LL * k;
      if (end < n) diff[(int)end] -= need;
    }
  }
  return true;
}

long long solve(int n, long long m, int k, const vector<long long>& a) {
  // 二分最终最小值
  long long lo = a[0];
  for (int i = 1; i < n; i++) lo = min(lo, a[i]);
  long long hi = lo + m, ans = lo;
  while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;
    if (can_reach(n, a, m, k, mid)) {
      ans = mid;
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return ans;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  // 第一行 n,m,k，第二行 n 个数
  int n, k;
  long long m;
  cin >> n >> m >> k;
  vector<long long> a(n);
  for (int i = 0; i < n; i++) cin >> a[i];
  cout << solve(n, m, k, a) << "\n";
  return 0;
}
