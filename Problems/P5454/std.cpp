#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

// 枚举每个探测原点，按平方距离分桶，同一桶内 c 个点贡献 c*(c-1) 组有序对
long long countEquidistant(const vector<pair<int, int>>& loc) {
    int m = (int)loc.size();
    long long ans = 0;
    // 每个点都当一次探测原点
    for (int p = 0; p < m; p++) {
        unordered_map<long long, int> buckets;
        buckets.reserve(m);
        int ux = loc[p].first;
        int uy = loc[p].second;
        for (int q = 0; q < m; q++) {
            if (p == q) {
                continue;
            }
            // 先转成 long long 再乘，否则 dx*dx 在 int 里会溢出
            long long dx = (long long)loc[q].first - ux;
            long long dy = (long long)loc[q].second - uy;
            long long d2 = dx * dx + dy * dy;
            buckets[d2]++;
        }
        // 同一距离有 c 个点：有序对 (q, r) 共 c*(c-1) 种
        for (auto& kv : buckets) {
            long long c = kv.second;
            ans += c * (c - 1);
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m;
    cin >> m;
    vector<pair<int, int>> loc(m);
    // 读入 m 座雷达站的坐标
    for (int i = 0; i < m; i++) {
        cin >> loc[i].first >> loc[i].second;
    }
    cout << countEquidistant(loc) << '\n';
    return 0;
}
