#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;
    const int U = 500000;

    vector<int> freq(U + 1, 0);
    for (int i = 0; i < n; ++i) {
        int a; cin >> a;
        ++freq[a]; // 统计每个分数出现次数
    }

    vector<int> divCnt(U + 1, 0), mulCnt(U + 1, 0);

    // 预处理 divCnt[x] = ∑_{d|x} freq[d]
    for (int d = 1; d <= U; ++d) {
        if (freq[d] == 0) continue; // 小优化
        for (int x = d; x <= U; x += d) {
            divCnt[x] += freq[d];
        }
    }

    // 预处理 mulCnt[x] = ∑_{k>=1} freq[k*x] = ∑_{x|j} freq[j]
    for (int x = 1; x <= U; ++x) {
        for (int j = x; j <= U; j += x) {
            mulCnt[x] += freq[j];
        }
    }

    // 处理查询
    while (m--) {
        int x; cin >> x;
        int ans = divCnt[x] + mulCnt[x] - freq[x];
        cout << ans << '\n';
    }
    return 0;
}
