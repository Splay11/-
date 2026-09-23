#include <iostream>
#include <vector>
using namespace std;

// 环形加油站：总油不够则无解；否则扫一遍，油箱为负就改起点
int solve(const vector<int>& gas, const vector<int>& cost) {
    int n = (int)gas.size();
    long long total = 0;
    long long tank = 0;
    int start = 0;
    for (int i = 0; i < n; i++) {
        // total 看整圈油是否够；tank 看当前起点走到 i 会不会没油
        long long diff = (long long)gas[i] - cost[i];
        total += diff;
        tank += diff;
        if (tank < 0) {
            // 从旧起点到 i 这段补不回来，只能从 i+1 重新出发
            start = i + 1;
            tank = 0;
        }
    }
    // 总油不够则任何起点都会失败；题目保证有解时起点唯一
    if (total < 0) {
        return -1;
    }
    return start;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> gas(n), cost(n);
    for (int i = 0; i < n; i++) {
        cin >> gas[i];
    }
    for (int i = 0; i < n; i++) {
        cin >> cost[i];
    }
    cout << solve(gas, cost) << '\n';
    return 0;
}
