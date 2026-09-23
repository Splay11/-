#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;

// 按开始时间排序后，检查是否有一场在上一场结束前就开始
bool canAttendAll(vector<pair<int, int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    for (int i = 1; i < (int)intervals.size(); i++) {
        // 当前场开始时间若早于上一场结束时间，两场有重叠
        if (intervals[i].first < intervals[i - 1].second) {
            return false;
        }
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int, int>> intervals(n);
    for (int i = 0; i < n; i++) {
        cin >> intervals[i].first >> intervals[i].second;
    }
    cout << (canAttendAll(intervals) ? "YES" : "NO") << '\n';
    return 0;
}
