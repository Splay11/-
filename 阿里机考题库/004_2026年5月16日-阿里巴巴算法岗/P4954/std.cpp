#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, r;
    string z;
    cin >> m >> r >> z;
    // 用有序集合维护所有 '0' 的位置，并加哨兵
    set<int> zeros;
    zeros.insert(0);
    zeros.insert(m + 1);
    long long w = 0;
    for (int i = 1; i <= m; ++i) {
        if (z[i - 1] == '0') zeros.insert(i);
    }
    // 初始权值：每段连续 1 的贡献 len*(len+1)/2
    int i = 1;
    while (i <= m) {
        if (z[i - 1] == '0') {
            ++i;
            continue;
        }
        int j = i;
        while (j <= m && z[j - 1] == '1') ++j;
        long long len = j - i;
        w += len * (len + 1) / 2;
        i = j;
    }

    while (r--) {
        int p;
        cin >> p;
        if (z[p - 1] == '0') {
            // 0→1：合并左右 1 段，权值增加 (a+1)*(b+1)
            auto it = zeros.find(p);
            auto il = prev(it);
            auto ir = next(it);
            long long a = p - *il - 1;
            long long b = *ir - p - 1;
            w += (a + 1) * (b + 1);
            zeros.erase(it);
            z[p - 1] = '1';
        } else {
            // 1→0：拆段，权值减少 (a+1)*(b+1)
            auto it = zeros.lower_bound(p);
            auto ir = it;
            auto il = prev(it);
            long long a = p - *il - 1;
            long long b = *ir - p - 1;
            w -= (a + 1) * (b + 1);
            zeros.insert(p);
            z[p - 1] = '0';
        }
        cout << w << '\n';
    }
    return 0;
}
