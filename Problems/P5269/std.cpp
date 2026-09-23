#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

long long solve(vector<int> a) {
    int n = (int)a.size();
    if (n == 1) return 0;
    sort(a.begin(), a.end(), greater<int>());
    if (a[0] <= 0) return 1LL * a[0] * (n - 1);
    long long ans = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] <= 0) break;
        ans += 1LL * a[i] * (n - 1 - i);
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
