#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    int solve(int n, int k, vector<pair<int, int>>& intervals) {
        sort(intervals.begin(), intervals.end());
        int start = 0;
        priority_queue<int, vector<int>, greater<int>> heap;
        int idx = 0;
        int ans = 0;

        while (idx < n || !heap.empty()) {
            while (!heap.empty() && heap.top() < start) {
                heap.pop();
            }

            while (idx < n && intervals[idx].first <= start) {
                heap.push(intervals[idx].second);
                idx++;
            }

            if (heap.empty()) {
                if (idx == n) {
                    break;
                }
                start = max(start, intervals[idx].first);
            }

            while (idx < n && intervals[idx].first <= start) {
                heap.push(intervals[idx].second);
                idx++;
            }

            for (int i = 0; i < k; ++i) {
                if (!heap.empty()) {
                    ans++;
                    heap.pop();
                }
            }

            start++;
        }

        return ans;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<pair<int, int>> intervals(n);
    for (int i = 0; i < n; ++i) {
        cin >> intervals[i].first >> intervals[i].second;
    }

    Solution solution;
    cout << solution.solve(n, k, intervals);
    return 0;
}
