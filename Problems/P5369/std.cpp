#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

const int MOD = 998244353;

int count_arrangements(int d, vector<int> a) {
    // 按高度排序后，从矮到高：每人对应后缀里「高度不超过自己+d」的可选人数
    // 嵌套后继集合上的哈密顿路条数等于这些人数的乘积
    sort(a.begin(), a.end());
    int n = (int)a.size();
    long long ans = 1;
    int j = 0;
    for (int i = 0; i < n; i++) {
        // j 右移到第一个高度大于 a[i]+d 的位置
        while (j < n && a[j] - a[i] <= d) {
            j++;
        }
        // 后缀 a[i..] 里高度仍不超过 a[i]+d 的人数
        ans = ans * (j - i) % MOD;
    }
    return (int)ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int m, d;
    cin >> m >> d;
    vector<int> v(m);
    for (int i = 0; i < m; i++) {
        cin >> v[i];
    }
    cout << count_arrangements(d, v) << "\n";
    return 0;
}
