#include <bits/stdc++.h>
using namespace std;

// 单调双端队列求一维窗口最大值
vector<long long> sliding_max_1d(const vector<long long>& arr, int k) {
    int n = (int)arr.size();
    vector<long long> res(n - k + 1);
    deque<int> dq;
    for (int i = 0; i < n; ++i) {
        while (!dq.empty() && arr[dq.back()] <= arr[i]) {
            dq.pop_back();
        }
        dq.push_back(i);
        if (dq.front() <= i - k) {
            dq.pop_front();
        }
        if (i >= k - 1) {
            res[i - k + 1] = arr[dq.front()];
        }
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, k;
    cin >> n >> m >> k;
    vector<vector<long long>> mat(n, vector<long long>(m));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            cin >> mat[i][j];
        }
    }
    // 先对每一行做长度为 k 的滑动窗口最大值
    vector<vector<long long>> row_max(n);
    for (int i = 0; i < n; ++i) {
        row_max[i] = sliding_max_1d(mat[i], k);
    }
    int cols = m - k + 1;
    int rows = n - k + 1;
    vector<vector<long long>> ans(rows, vector<long long>(cols));
    for (int j = 0; j < cols; ++j) {
        vector<long long> col(n);
        for (int i = 0; i < n; ++i) {
            col[i] = row_max[i][j];
        }
        vector<long long> col_res = sliding_max_1d(col, k);
        for (int i = 0; i < rows; ++i) {
            ans[i][j] = col_res[i];
        }
    }
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            if (j) {
                cout << ' ';
            }
            cout << ans[i][j];
        }
        cout << "\n";
    }
    return 0;
}
