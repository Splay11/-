#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

long long min_swaps(const string& d) {
    // 环上把 0 挪到偶数位或奇数位；只允许循环错位，不能交叉
    int len = (int)d.size();
    int m = len / 2;
    vector<int> pos;
    for (int i = 0; i < len; i++) {
        if (d[i] == '0') {
            pos.push_back(i);
        }
    }
    long long ans = (1LL << 62);
    for (int start = 0; start <= 1; start++) {
        // b[i]：第 i 个 0 相对第 i 个目标格的有向偏移
        vector<long long> a;
        for (int i = 0; i < m; i++) {
            long long b = (long long)pos[i] - 2LL * i - start;
            a.push_back(-b);
        }
        sort(a.begin(), a.end());
        vector<long long> pref(m + 1, 0);
        for (int i = 0; i < m; i++) {
            pref[i + 1] = pref[i] + a[i];
        }
        for (int k = -(m - 1); k <= m - 1; k++) {
            // x = 2k，求点集 a 到 x 的曼哈顿和
            long long x = 2LL * k;
            int left = (int)(upper_bound(a.begin(), a.end(), x) - a.begin());
            long long cur = x * left - pref[left] + (pref[m] - pref[left]) - x * (m - left);
            if (cur < ans) {
                ans = cur;
            }
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int m;
    cin >> m;
    string d;
    cin >> d;
    cout << min_swaps(d) << endl;
    return 0;
}
