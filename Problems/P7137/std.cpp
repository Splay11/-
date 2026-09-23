#include <iostream>
#include <vector>
using namespace std;

// 判断每段长度为 length 时，能不能切出至少 k 段
// 段数可能到 1e14，用 long long，累加到 >= k 就提前停
bool canCut(const vector<int>& a, long long k, int length) {
    long long got = 0;
    for (int i = 0; i < (int)a.size(); i++) {
        got += a[i] / length;
        if (got >= k) {
            return true;
        }
    }
    return false;
}

// 二分答案：长度越大越难切够 k 段。题目保证长度为 1 一定可行
int solve(const vector<int>& a, long long k) {
    int left = 1;
    int right = a[0];
    for (int i = 1; i < (int)a.size(); i++) {
        if (a[i] > right) {
            right = a[i];
        }
    }
    int ans = 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (canCut(a, k, mid)) {
            // mid 可行，试更长的
            ans = mid;
            left = mid + 1;
        } else {
            // mid 太长，切不够，往短了找
            right = mid - 1;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long k;
    cin >> n >> k;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    cout << solve(a, k) << '\n';
    return 0;
}
