#include <bits/stdc++.h>
using namespace std;

// 统计交叉表 pulse[i] * gauge[j] >= bound 的格子数
long long countPairs(vector<long long>& pulse, vector<long long>& gauge, long long bound) {
    sort(gauge.begin(), gauge.end());
    int C = (int)gauge.size();
    long long ans = 0;

    for (long long p : pulse) {
        if (bound == 0) {
            // bound 为 0 时，非负乘积均达标
            ans += C;
        } else if (p == 0) {
            // pulse 为 0 且 bound > 0 时无法达标
            continue;
        } else {
            // 需要 gauge >= ceil(bound / pulse)
            long long need = (bound + p - 1) / p;
            int pos = lower_bound(gauge.begin(), gauge.end(), need) - gauge.begin();
            ans += C - pos;
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
        int R, C;
        long long bound;
        cin >> R >> C >> bound;

        vector<long long> pulse(R), gauge(C);
        for (int i = 0; i < R; i++) cin >> pulse[i];
        for (int j = 0; j < C; j++) cin >> gauge[j];

        cout << countPairs(pulse, gauge, bound) << '\n';
    }

    return 0;
}
