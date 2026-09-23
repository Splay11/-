#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;

long long path_sum(long long p) {
    // S(p) = sum_{j=1}^{p} 2^{ctz(j)}
    // i ⊕ (i+1) = 2^{ctz(i+1)+1} - 1，故答案为 2*S(p) - p - 1
    long long s = 0;
    for (int k = 0; k <= 60; k++) {
        long long pk = 1LL << k;
        if (pk > p) {
            break;
        }
        // ctz = k 的个数是 floor(p/2^k) - floor(p/2^{k+1})
        long long diff = (p >> k) - (p >> (k + 1));
        s += pk % MOD * (diff % MOD) % MOD;
        if (s >= MOD) {
            s -= MOD;
        }
    }
    long long ans = (2 * s % MOD - p % MOD - 1) % MOD;
    if (ans < 0) {
        ans += MOD;
    }
    return ans;
}

int main() {
    // 询问数可能到 200000，关闭同步以免读入超时
    ios::sync_with_stdio(false);
    cin.tie(0);
    int q;
    cin >> q;
    for (int i = 0; i < q; i++) {
        long long p;
        cin >> p;
        cout << path_sum(p) << "\n";
    }
    return 0;
}
