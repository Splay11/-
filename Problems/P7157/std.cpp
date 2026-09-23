#include <iostream>
#include <vector>
#include <algorithm>
#include <utility>
using namespace std;

// 按右端点排序后贪心保留，最少删除 = n - 最多保留
int solve(vector<pair<int, int> >& intervals) {
    sort(intervals.begin(), intervals.end(),
         [](const pair<int, int>& a, const pair<int, int>& b) {
             return a.second < b.second;
         });
    int keep = 0;
    int last_end = -1000000000;
    for (int i = 0; i < (int)intervals.size(); i++) {
        int start = intervals[i].first;
        int end = intervals[i].second;
        // 左端点不小于已保留的右端点，只在端点相碰也算不重叠
        if (start >= last_end) {
            keep++;
            last_end = end;
        }
    }
    return (int)intervals.size() - keep;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int, int> > intervals(n);
    for (int i = 0; i < n; i++) {
        cin >> intervals[i].first >> intervals[i].second;
    }
    cout << solve(intervals) << '\n';
    return 0;
}
