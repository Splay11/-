#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

bool cmpGroup(const vector<long long>& a, const vector<long long>& b) {
    return a[0] > b[0];
}

// 枚举最终种类数：按每种最大价值从大到小加入，续选部分用堆维护前 r 大
long long maxScore(const vector<int>& types, const vector<int>& values, int k) {
    int n = (int)types.size();
    vector<pair<int, int> > flowers(n);
    for (int i = 0; i < n; i++) {
        flowers[i] = make_pair(types[i], values[i]);
    }
    sort(flowers.begin(), flowers.end());
    vector<vector<long long> > arr;
    int i = 0;
    while (i < n) {
        int j = i;
        vector<long long> vs;
        while (j < n && flowers[j].first == flowers[i].first) {
            vs.push_back(flowers[j].second);
            j++;
        }
        sort(vs.begin(), vs.end());
        reverse(vs.begin(), vs.end());
        arr.push_back(vs);
        i = j;
    }
    sort(arr.begin(), arr.end(), cmpGroup);

    long long ans = 0;
    bool found = false;
    priority_queue<long long> extras;
    priority_queue<long long, vector<long long>, greater<long long> > used;
    long long sumUsed = 0;
    long long head = 0;
    int total = 0;
    int d = 0;
    for (size_t gi = 0; gi < arr.size(); gi++) {
        d++;
        // 选中这一种：必须拿它最贵的一朵，剩下的进备用堆
        head += arr[gi][0];
        total += (int)arr[gi].size();
        for (size_t p = 1; p < arr[gi].size(); p++) {
            extras.push(arr[gi][p]);
        }
        int r = k - d;
        if (r < 0) {
            break;
        }
        // used 里只保留当前还需要的 r 朵「同种续选」
        while (!used.empty() && (int)used.size() > r) {
            long long x = used.top();
            used.pop();
            sumUsed -= x;
            extras.push(x);
        }
        while (!extras.empty() && (int)used.size() < r) {
            long long x = extras.top();
            extras.pop();
            used.push(x);
            sumUsed += x;
        }
        while (!extras.empty() && !used.empty() && extras.top() > used.top()) {
            long long bad = used.top();
            used.pop();
            sumUsed -= bad;
            long long good = extras.top();
            extras.pop();
            used.push(good);
            sumUsed += good;
            extras.push(bad);
        }
        // 已选种类凑得出 k 朵时，更新答案：价值和 + 种类平方
        if (total >= k && (int)used.size() == r) {
            long long cur = head + sumUsed + 1LL * d * d;
            if (!found || cur > ans) {
                ans = cur;
                found = true;
            }
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    // 第一行 n、k，随后两行分别是类型和价值
    int n, k;
    cin >> n >> k;
    vector<int> types(n), values(n);
    for (int i = 0; i < n; i++) {
        cin >> types[i];
    }
    for (int i = 0; i < n; i++) {
        cin >> values[i];
    }
    cout << maxScore(types, values, k) << "\n";
    return 0;
}
