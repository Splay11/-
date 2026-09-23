#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

// 任意划分的贡献之和不超过 (全局 max - 全局 min) * n，整段取满即可。
int64 max_fluctuation(int n, const vector<int64>& v) {
    int64 mn = v[0], mx = v[0];
    for (int i = 1; i < n; ++i) {
        mn = min(mn, v[i]);
        mx = max(mx, v[i]);
    }
    return (mx - mn) * n;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int64> v(n);
    for (int i = 0; i < n; ++i) {
        cin >> v[i];
    }
    cout << max_fluctuation(n, v) << '\n';
    return 0;
}
