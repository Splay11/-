#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1'000'000'007LL;
const long long INV2 = 500'000'004LL; // 2 的逆元

// S(m) = (m(m+1)/2)^2  (mod MOD)
long long sum_cubes(long long m) {
    if (m <= 0) return 0;
    m %= MOD;
    long long t = m * ((m + 1) % MOD) % MOD; // m(m+1)
    t = t * INV2 % MOD;                      // /2
    return (t * t) % MOD;                    // 平方
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n; 
    if (!(cin >> n)) return 0;

    long long ans = 0, L = 1;
    while (L <= n) {
        long long q = n / L;                 // 当前商
        long long R = n / q;                 // 该商的最右端
        long long seg = (sum_cubes(R) - sum_cubes(L - 1)) % MOD; // 区间立方和
        if (seg < 0) seg += MOD;
        ans = (ans + seg * (q % MOD)) % MOD;                    // 累加
        L = R + 1;                                              // 下一段
    }
    cout << (ans % MOD) << "\n";
    return 0;
}
