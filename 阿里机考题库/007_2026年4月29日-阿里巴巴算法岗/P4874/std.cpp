#include <bits/stdc++.h>
using namespace std;

// 计算最早空闲时刻：排序维护窗口后，找第一个不被任何窗口覆盖的非负整数
long long findEarliestFree(vector<pair<long long, long long>>& windows) {
    // 按窗口起点从小到大排序
    sort(windows.begin(), windows.end());

    // ans 表示当前最早可能空闲的时刻
    long long ans = 0;

    for (auto w : windows) {
        long long s = w.first;   // 窗口起点
        long long e = w.second;  // 窗口终点

        // 若当前窗口起点大于 ans，说明 ans 未被占用，即为答案
        if (s > ans) {
            break;
        }

        // 若 ans 落在当前窗口内，则把 ans 推进到窗口终点之后
        if (e >= ans) {
            ans = e + 1;
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<pair<long long, long long>> windows(n);

    // 读取 n 个维护窗口
    for (int i = 0; i < n; i++) {
        cin >> windows[i].first >> windows[i].second;
    }

    cout << findEarliestFree(windows) << '\n';

    return 0;
}
