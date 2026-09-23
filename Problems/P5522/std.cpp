#include <iostream>
#include <unordered_map>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long k;
    cin >> n >> k;
    unordered_map<long long, long long> cnt;
    cnt[0] = 1;  // 空前缀
    long long pref = 0, ans = 0;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        pref ^= x;
        // 子数组异或 = pref ^ pre == k
        ans += cnt[pref ^ k];
        cnt[pref]++;
    }
    cout << ans << '\n';
    return 0;
}
