// ACM 风格：从标准输入读取，输出结果
#include <bits/stdc++.h>
using namespace std;

static int countFactor(long long x, int p) {
    // 计算 x 中质因子 p (只会是 2 或 5)
    int c = 0;
    while (x % p == 0) {
        x /= p;
        c++;
    }
    return c;
}

long long solve(const vector<long long>& a, long long k) {
    int n = (int)a.size();
    vector<int> c2(n), c5(n);
    for (int i = 0; i < n; ++i) {
        c2[i] = countFactor(a[i], 2);
        c5[i] = countFactor(a[i], 5);
    }
    long long ans = 0;
    int l = 0, r = 0;
    long long cur2 = 0, cur5 = 0;
    // 滑动窗口 [l, r)
    while (l < n) {
        while (r < n && (cur2 < k || cur5 < k)) {
            cur2 += c2[r];
            cur5 += c5[r];
            ++r;
        }
        if (cur2 >= k && cur5 >= k) {
            ans += (n - r + 1);
        }
        cur2 -= c2[l];
        cur5 -= c5[l];
        ++l;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long k;
    if (!(cin >> n >> k)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    cout << solve(a, k) << "\n";
    return 0;
}
