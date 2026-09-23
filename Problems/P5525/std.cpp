#include <bits/stdc++.h>
using namespace std;

// 质因数分解，返回质数积与指数
pair<long long, vector<int>> factorize(long long n) {
    long long prod = 1;
    vector<int> exps;
    for (long long d = 2; d * d <= n; ++d) {
        if (n % d == 0) {
            prod *= d;
            int cnt = 0;
            while (n % d == 0) {
                n /= d;
                ++cnt;
            }
            exps.push_back(cnt);
        }
    }
    if (n > 1) {
        prod *= n;
        exps.push_back(1);
    }
    return {prod, exps};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n;
    cin >> n;
    if (n == 1) {
        cout << "1 0\n";
        return 0;
    }
    pair<long long, vector<int>> fac = factorize(n);
    long long mn = fac.first;
    vector<int>& exps = fac.second;
    int max_e = *max_element(exps.begin(), exps.end());
    // 找到 >= max_e 的最小 2 的幂
    long long pw = 1;
    int k = 0;
    while (pw < max_e) {
        pw *= 2;
        ++k;
    }
    bool need_mul = false;
    for (size_t i = 0; i < exps.size(); ++i) {
        if (exps[i] != pw) {
            need_mul = true;
            break;
        }
    }
    int ops = k + (need_mul ? 1 : 0);
    cout << mn << ' ' << ops << '\n';
    return 0;
}
