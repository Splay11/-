#include <deque>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

const long long INF = (long long)4e18;

// 空队列用一行单独的 0 表示
bool isEmpty(const vector<int>& arr) {
    return arr.empty() || (arr.size() == 1 && arr[0] == 0);
}

// 连续放掉不超过 lim，刚好接 t 项的最小耗时
long long minCost(const vector<int>& arr, int t, int lim) {
    int n = (int)arr.size();
    if (n == 0) {
        return 0;
    }
    if (t == 0) {
        return n <= lim ? 0 : -1;
    }
    if (t > n) {
        return -1;
    }
    if (n - t > (t + 1) * 1LL * lim) {
        return -1;
    }

    vector<long long> dp(n, INF);
    for (int i = 0; i < n; i++) {
        if (i <= lim) {
            dp[i] = arr[i];
        }
    }

    // 第 2..t 次接单：上一层下标落在 [i-lim-1, i-1] 内取最小
    for (int k = 2; k <= t; k++) {
        vector<long long> ndp(n, INF);
        deque<int> dq;
        for (int i = 0; i < n; i++) {
            int prev = i - 1;
            if (prev >= 0 && dp[prev] < INF) {
                while (!dq.empty() && dp[dq.back()] >= dp[prev]) {
                    dq.pop_back();
                }
                dq.push_back(prev);
            }
            int lo = i - lim - 1;
            while (!dq.empty() && dq.front() < lo) {
                dq.pop_front();
            }
            if (!dq.empty()) {
                ndp[i] = dp[dq.front()] + arr[i];
            }
        }
        dp.swap(ndp);
    }

    long long ans = INF;
    for (int i = 0; i < n; i++) {
        if (n - 1 - i <= lim && dp[i] < ans) {
            ans = dp[i];
        }
    }
    return ans >= INF ? -1 : ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> arr;
    int x;
    while (ss >> x) {
        arr.push_back(x);
    }
    if (isEmpty(arr)) {
        cout << 0 << '\n';
        return 0;
    }
    int t, lim;
    cin >> t >> lim;
    cout << minCost(arr, t, lim) << '\n';
    return 0;
}
