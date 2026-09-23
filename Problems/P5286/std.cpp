#include <bits/stdc++.h>
using namespace std;

long long solve(int n, long long k, const vector<long long>& a) {
  unordered_map<long long, int> cnt;
  cnt.reserve(n * 2);
  for (long long x : a) cnt[x]++;
  long long ans = 0;
  unordered_set<long long> seen;
  seen.reserve(cnt.size() * 2);
  for (auto& e : cnt) {
    long long x = e.first;
    if (seen.count(x)) continue;
    long long y = k - x;
    if (x == y) {
      ans += max(0, e.second - 1);
      seen.insert(x);
    } else {
      auto it = cnt.find(y);
      if (it != cnt.end()) {
        ans += min(e.second, it->second);
        seen.insert(x);
        seen.insert(y);
      }
    }
  }
  return ans;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long k;
  cin >> n >> k;
  vector<long long> a(n);
  for (int i = 0; i < n; i++) cin >> a[i];
  cout << solve(n, k, a) << "\n";
  return 0;
}
