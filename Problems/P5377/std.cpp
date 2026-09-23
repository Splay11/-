#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

// 每人价值都是 1，按驻场总耗材从小到大批准
int max_accept(int n, long long b, const vector<int>& v) {
    vector<long long> costs(n);
    for (int i = 0; i < n; i++) {
        // 下标从 0 计：从当天到第 n 天共 (n-i) 天
        costs[i] = 1LL * v[i] * (n - i);
    }
    sort(costs.begin(), costs.end());
    long long used = 0;
    int ans = 0;
    for (int i = 0; i < n; i++) {
        if (used + costs[i] <= b) {
            used += costs[i];
            ans++;
        } else {
            break;
        }
    }
    return ans;
}

int main() {
    int n;
    long long b;
    cin >> n >> b;
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin >> v[i];
    }
    cout << max_accept(n, b, v) << '\n';
    return 0;
}
