#include <iostream>
#include <vector>
using namespace std;

// 埃氏筛统计严格小于 n 的质数个数
int solve(int n) {
    if (n <= 2) {
        return 0;
    }
    vector<char> is_prime(n, 1);
    is_prime[0] = 0;
    is_prime[1] = 0;
    for (int i = 2; 1LL * i * i < n; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j < n; j += i) {
                is_prime[j] = 0;
            }
        }
    }
    int ans = 0;
    for (int i = 2; i < n; i++) {
        if (is_prime[i]) {
            ans++;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    cout << solve(n) << '\n';
    return 0;
}
