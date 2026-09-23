#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;

long long min_range(const vector<long long>& v) {
    // 枚举左右两半的分界，两半内部再各切一刀
    // 正数前缀和严格递增：半段内最优切点随边界右移只向右走
    int n = (int)v.size();
    vector<long long> s(n + 1, 0);
    for (int t = 0; t < n; t++) {
        s[t + 1] = s[t] + v[t];
    }
    long long total = s[n];
    long long ans = total;
    int i = 1;
    int k = 3;
    // j 是第二段结尾下标（第 1..j 个为左半，至少 2 个，右边也至少 2 个）
    for (int j = 2; j <= n - 2; j++) {
        // 左半切点 i∈[1,j-1]，让两段和尽量接近 s[j]/2
        if (i > j - 1) {
            i = j - 1;
        }
        while (i + 1 <= j - 1 && llabs(2 * s[i + 1] - s[j]) <= llabs(2 * s[i] - s[j])) {
            i++;
        }
        // 右半切点 k∈[j+1,n-1]，让两段和尽量接近剩余一半
        if (k <= j) {
            k = j + 1;
        }
        while (k + 1 <= n - 1 &&
               llabs(2 * (s[k + 1] - s[j]) - (total - s[j])) <= llabs(2 * (s[k] - s[j]) - (total - s[j]))) {
            k++;
        }
        long long a = s[i];
        long long b = s[j] - s[i];
        long long c = s[k] - s[j];
        long long d = total - s[k];
        long long mx = max(max(a, b), max(c, d));
        long long mn = min(min(a, b), min(c, d));
        if (mx - mn < ans) {
            ans = mx - mn;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int m;
    cin >> m;
    vector<long long> v(m);
    for (int t = 0; t < m; t++) {
        cin >> v[t];
    }
    cout << min_range(v) << "\n";
    return 0;
}
