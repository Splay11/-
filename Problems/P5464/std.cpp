#include <iostream>
#include <vector>
using namespace std;

const long long NEG = -(1LL << 60);

// 三段 DP：尚未加速 / 正在加速 / 加速已结束
// d0 整段没加速；d1 当前项在窗口内；d2 窗口已结束
long long maxGain(const vector<long long>& v) {
    long long d0 = v[0];
    long long d1 = 2 * v[0];
    long long d2 = NEG;
    long long ans = d0 > d1 ? d0 : d1;
    int m = (int)v.size();
    for (int i = 1; i < m; i++) {
        long long x = v[i];
        long long t = 2 * x;
        // 不加速
        long long nd0 = x > d0 + x ? x : d0 + x;
        // 正在加速：新开窗口 / 转入 / 继续
        long long nd1 = t;
        if (d0 + t > nd1) {
            nd1 = d0 + t;
        }
        if (d1 + t > nd1) {
            nd1 = d1 + t;
        }
        // 加速已结束，只能加原值
        long long nd2 = d1 + x;
        if (d2 + x > nd2) {
            nd2 = d2 + x;
        }
        d0 = nd0;
        d1 = nd1;
        d2 = nd2;
        if (d0 > ans) {
            ans = d0;
        }
        if (d1 > ans) {
            ans = d1;
        }
        if (d2 > ans) {
            ans = d2;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    // 第一行组数；每组先读 m 再读 m 个收益
    int k;
    cin >> k;
    vector<long long> ans;
    ans.reserve(k);
    for (int t = 0; t < k; t++) {
        int m;
        cin >> m;
        vector<long long> v(m);
        for (int i = 0; i < m; i++) {
            cin >> v[i];
        }
        ans.push_back(maxGain(v));
    }
    // 一行输出 k 个答案，空格隔开
    for (int i = 0; i < k; i++) {
        if (i) {
            cout << ' ';
        }
        cout << ans[i];
    }
    cout << "\n";
    return 0;
}
