#include <iostream>
#include <vector>
using namespace std;

const long long MOD = 1000000007;

// 计算 H(d)=sum (i mod d)*v[i] （d=1..n），答案对 MOD 取模
vector<long long> phase_contrib(int n, const vector<long long>& v) {
    // n=1 时倍数循环不进入，H(1)=0，与 0 mod 1 = 0 一致
    // 后缀和：suf[i] = v[i]+...+v[n-1]（已取模）
    vector<long long> suf(n + 1, 0);
    for (int i = n - 1; i >= 0; i--) {
        suf[i] = suf[i + 1] + v[i];
        if (suf[i] >= MOD) suf[i] -= MOD;
    }
    // S = sum i*v[i]；由 i mod d = i - d*floor(i/d) 得 H(d)=S-d*g(d)
    long long S = 0;
    for (int i = 0; i < n; i++) {
        S = (S + 1LL * i % MOD * (v[i] % MOD)) % MOD;
    }
    vector<long long> ans(n);
    for (int d = 1; d <= n; d++) {
        long long g = 0;
        // 枚举 m*d < n 的倍数，调和级数合计 O(n log n)
        for (int md = d; md < n; md += d) {
            g += suf[md];
            if (g >= MOD) g -= MOD;
        }
        ans[d - 1] = (S - 1LL * d % MOD * g % MOD + MOD) % MOD;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;  // 彩灯盏数
    vector<long long> v(n);
    for (int i = 0; i < n; i++) {
        cin >> v[i];  // 第 i 盏标定亮度
    }
    vector<long long> ans = phase_contrib(n, v);
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
