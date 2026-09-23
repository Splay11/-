#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

// 判定是否存在长度 >= w 的窗口，使 floor(sum/len) >= x
bool feasible(const vector<long long>& vals, int w, long long x) {
    int m = (int)vals.size();
    vector<long long> pre(m + 1, 0);
    for (int i = 0; i < m; i++) {
        // 用 64 位：v_p 与 x 最大约 1e9，前缀可达 n*2e9
        pre[i + 1] = pre[i] + (vals[i] - x);
    }
    // mn 是 pre[0..r-w] 的最小值，对应右端点为 r 且长度至少 w 的窗口
    long long mn = pre[0];
    for (int r = w; r <= m; r++) {
        if (pre[r - w] < mn) {
            mn = pre[r - w];
        }
        if (pre[r] - mn >= 0) {
            return true;
        }
    }
    return false;
}

// 二分最大班均净值，搜索区间为 [min v, max v]
long long maxFloorAvg(const vector<long long>& vals, int w) {
    long long lo = *min_element(vals.begin(), vals.end());
    long long hi = *max_element(vals.begin(), vals.end());
    long long ans = lo;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (feasible(vals, w, mid)) {
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int g;
    cin >> g;
    vector<long long> answers;
    answers.reserve(g);
    for (int t = 0; t < g; t++) {
        int m, w;
        // m 与 w 各占一行，>> 会自动跳过换行
        cin >> m >> w;
        string line;
        getline(cin, line);
        if (line.empty()) {
            getline(cin, line);
        }
        // 把逗号换成空格再按整数解析
        replace(line.begin(), line.end(), ',', ' ');
        stringstream ss(line);
        vector<long long> vals;
        vals.reserve(m);
        long long x;
        while (ss >> x) {
            vals.push_back(x);
        }
        answers.push_back(maxFloorAvg(vals, w));
    }
    for (int i = 0; i < g; i++) {
        if (i) {
            cout << ' ';
        }
        cout << answers[i];
    }
    cout << '\n';
    return 0;
}
