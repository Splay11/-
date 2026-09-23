#include <bits/stdc++.h>
using namespace std;

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int T;
	if (!(cin >> T)) return 0;
	while (T--) {
		int n;
		cin >> n;
		vector<long long> a(n);
		for (int i = 0; i < n; ++i) cin >> a[i];
		sort(a.rbegin(), a.rend()); // 降序

		vector<char> used(n + 1, 0);
		bool ok = true;
		for (long long x : a) {
			while (x > n || (x > 0 && used[(int)x])) x >>= 1; 
			if (x == 0) { ok = false; break; }
			used[(int)x] = 1;
		}
		cout << (ok ? "YES" : "NO") << '\n';
	}
	return 0;
}
