#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<int> solve(int n, int k, int S, int R) {
    for (int M = 1; M <= 6; M++) {
        // 检查保留部分范围
        if (R < n - k || R > (ll)(n - k) * M) continue;
        // 检查召回部分范围
        ll diff = (ll)S - R;
        if (diff < (ll)k * M || diff > (ll)k * 6) continue;

        // 构造保留部分
        vector<int> ans;
        ll extra = (ll)R - (n - k);
        for (int i = 0; i < n - k; i++) {
            int add = (int)min(extra, (ll)M - 1);
            ans.push_back(1 + add);
            extra -= add;
        }

        // 构造召回部分
        extra = diff - (ll)k * M;
        for (int i = 0; i < k; i++) {
            int add = (int)min(extra, (ll)6 - M);
            ans.push_back(M + add);
            extra -= add;
        }
        return ans;
    }
    return {};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k, S, R;
    cin >> n >> k >> S >> R;
    auto ans = solve(n, k, S, R);
    if (ans.empty()) {
        cout << "-1\n";
    } else {
        for (int i = 0; i < (int)ans.size(); i++) {
            if (i > 0) cout << ' ';
            cout << ans[i];
        }
        cout << '\n';
    }
    return 0;
}
