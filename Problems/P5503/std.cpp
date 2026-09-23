#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, k;
    cin >> n >> m >> k;
    // 展平后排序取第 K 大；总元素不超过 500*500
    vector<long long> vals;
    vals.reserve(n * m);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            long long x;
            cin >> x;
            vals.push_back(x);
        }
    }
    sort(vals.begin(), vals.end(), greater<long long>());
    cout << vals[k - 1] << "\n";
    return 0;
}
