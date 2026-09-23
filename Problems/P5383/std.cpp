#include <iostream>
#include <vector>
using namespace std;

// 统计无序对 (i,j) 使得 (w[i]+w[j]) % t == 0
long long count_pairs(int n, int t, const vector<long long>& w) {
    vector<long long> cnt(t, 0);
    for (int i = 0; i < n; i++) {
        cnt[w[i] % t]++;  // 按余数分桶
    }
    long long ans = 0;
    // 余数 0 只能和同类配对
    ans += cnt[0] * (cnt[0] - 1) / 2;
    // t 为偶数时，余数 t/2 也只能和同类配对
    if (t % 2 == 0) {
        long long half = cnt[t / 2];
        ans += half * (half - 1) / 2;
    }
    // r 与 t-r 互补，每对余数类只乘一次，避免算重
    for (int r = 1; r < (t + 1) / 2; r++) {
        ans += cnt[r] * cnt[t - r];
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, t;
    cin >> n >> t;  // 件数、装载模数
    vector<long long> w(n);
    for (int i = 0; i < n; i++) {
        cin >> w[i];  // 第 i 件重量
    }
    cout << count_pairs(n, t, w) << '\n';
    return 0;
}
