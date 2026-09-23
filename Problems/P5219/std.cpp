#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

// 从右向左贪心：维护右侧块的代表值 suf，当前项过大则必须合并。
int64 min_merges(const vector<int64>& v) {
    int64 suf = LLONG_MAX;
    int64 ans = 0;
    for (int i = (int)v.size() - 1; i >= 0; --i) {
        if (v[i] <= suf) {
            suf = v[i];
        } else {
            ++ans;
            suf += v[i];
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    while (q--) {
        int n;
        cin >> n;
        vector<int64> v(n);
        for (int i = 0; i < n; ++i) {
            cin >> v[i];
        }
        cout << min_merges(v) << '\n';
    }
    return 0;
}
