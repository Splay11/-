#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;
const int MAXA = 100000;

int phi[MAXA + 1];

void initPhi() {
    for (int i = 0; i <= MAXA; i++) phi[i] = i;
    vector<char> vis(MAXA + 1, 0);
    for (int i = 2; i <= MAXA; i++) {
        if (vis[i]) continue;
        for (int j = i; j <= MAXA; j += i) {
            vis[j] = 1;
            phi[j] = phi[j] / i * (i - 1);
        }
    }
}

vector<int> divisors(int d) {
    vector<int> out;
    for (int t = 1; 1LL * t * t <= d; t++) {
        if (d % t == 0) {
            out.push_back(t);
            if (t * t != d) out.push_back(d / t);
        }
    }
    return out;
}

int prefix(long long n, int d) {
    if (n <= 0) return 0;
    long long s = 0;
    for (int x : divisors(d)) {
        s += 1LL * phi[x] % MOD * ((n / x) % MOD) % MOD;
        s %= MOD;
    }
    return (int)s;
}

int solve(int x, int y, long long left, long long right) {
    int d = x > y ? x - y : y - x;
    if (d == 0) {
        long long cnt = (right - left + 1) % MOD;
        long long term = ((2LL * x) % MOD + left % MOD + right % MOD) % MOD;
        return (int)(cnt * term % MOD * ((MOD + 1) / 2) % MOD);
    }
    long long lo = (long long)x + left;
    long long hi = (long long)x + right;
    int ans = prefix(hi, d) - prefix(lo - 1, d);
    if (ans < 0) ans += MOD;
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    initPhi();
    int k;
    cin >> k;
    while (k--) {
        int x, y;
        long long left, right;
        cin >> x >> y >> left >> right;
        cout << solve(x, y, left, right) << '\n';
    }
    return 0;
}
