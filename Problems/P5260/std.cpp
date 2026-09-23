#include <iostream>
#include <vector>
using namespace std;

long long solve(const vector<int>& a) {
    int n = (int)a.size();
    long long ans = 0;
    for (int l = 0; l < n; l++) {
        long long s = 0;
        int lim = min(n, l + 100);
        for (int r = l; r < lim; r++) {
            s += a[r];
            int L = r - l + 1;
            if (s == 1LL * L * L) ans++;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for (int i = 0; i < n; i++) cin >> a[i];
        cout << solve(a) << '\n';
    }
    return 0;
}
