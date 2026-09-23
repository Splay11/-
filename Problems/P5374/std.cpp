#include <iostream>
#include <vector>
using namespace std;

bool can_reach(int n, long long s, long long t, const vector<long long>& a) {
    // 物体总数必须对上；最少搬运次数是离开 1 号货位的件数
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        sum += a[i];
    }
    if (sum != s) {
        return false;
    }
    long long mn = s - a[0];
    if (t < mn) {
        return false;
    }
    long long extra = t - mn;
    // 刚好最少次数，无需浪费
    if (extra == 0) {
        return true;
    }
    // 没有货或只有一个货位时，多出来的步数走不了
    if (s == 0 || n == 1) {
        return false;
    }
    // 两个货位只能来回，浪费步数必须是偶数
    if (extra % 2 == 0) {
        return true;
    }
    // 奇数步浪费需要第三个货位绕一下；已经到位时无法只多走 1 步
    if (n < 3 || t == 1) {
        return false;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int n;
    long long s, t;
    cin >> n >> s >> t;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    if (can_reach(n, s, t, a)) {
        cout << "Yes\n";
    } else {
        cout << "No\n";
    }
    return 0;
}
