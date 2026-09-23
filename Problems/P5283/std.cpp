#include <bits/stdc++.h>
using namespace std;

int main() {
  int n;
  long long k;
  cin >> n >> k;
  map<long long, long long> mp;
  for (int i = 0; i < n; i++) {
    long long a, b;
    cin >> a >> b;
    mp[a] += b;
  }
  long long s = 0;
  for (auto& e : mp) s += e.second;
  if (s <= k) {
    cout << 0 << "\n";
    return 0;
  }
  for (auto& e : mp) {
    s -= e.second;
    if (s <= k) {
      cout << e.first + 1 << "\n";
      return 0;
    }
  }
  cout << mp.rbegin()->first + 1 << "\n";
  return 0;
}
