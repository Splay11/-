#include <bits/stdc++.h>
using namespace std;

int main() {
  int n;
  cin >> n;
  vector<int> e(n), a(n), b(n);
  for (int i = 0; i < n; i++) cin >> e[i];
  for (int i = 0; i < n; i++) cin >> a[i];
  for (int i = 0; i < n; i++) cin >> b[i];

  priority_queue<pair<int, long long>, vector<pair<int, long long>>, greater<pair<int, long long>>> pq;
  long long ans = 0;
  for (int i = 1; i <= n; i++) {
    int exp = e[i - 1] - 1;
    if (a[i - 1] > 0 && exp >= i) pq.push({exp, (long long)a[i - 1]});
    while (!pq.empty() && pq.top().first < i) pq.pop();
    long long need = b[i - 1];
    while (need > 0 && !pq.empty()) {
      auto [ex, cnt] = pq.top();
      pq.pop();
      if (ex < i) continue;
      long long take = min(need, cnt);
      need -= take;
      cnt -= take;
      if (cnt > 0) pq.push({ex, cnt});
    }
    ans += need;
  }
  cout << ans << "\n";
  return 0;
}
