#include <bits/stdc++.h>
using namespace std;

int main() {
  int n;
  long long A, B;
  cin >> n >> A >> B;
  long long ca = 0, cb = 0;
  for (int i = 0; i < n; i++) {
    long long x;
    cin >> x;
    if (x == A) ca++;
    if (x == B) cb++;
  }
  double ans = 1.0 * n * n / (ca * cb);
  cout << fixed << setprecision(1) << ans << "\n";
  return 0;
}
