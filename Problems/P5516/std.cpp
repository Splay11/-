#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    vector<int> left(n, 1), right(n, 1);
    // 以 i 结尾的最长严格递增
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (a[j] < a[i]) left[i] = max(left[i], left[j] + 1);
        }
    }
    // 以 i 开头的最长严格递减
    for (int i = n - 1; i >= 0; i--) {
        for (int j = i + 1; j < n; j++) {
            if (a[j] < a[i]) right[i] = max(right[i], right[j] + 1);
        }
    }
    int ans = 0;
    for (int i = 0; i < n; i++) {
        if (left[i] >= 2 && right[i] >= 2) {
            ans = max(ans, left[i] + right[i] - 1);
        }
    }
    cout << ans << "\n";
    return 0;
}
