#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

bool cmpBoat(const pair<int, int>& x, const pair<int, int>& y) {
    if (x.first != y.first) {
        return x.first < y.first;
    }
    return x.second > y.second;
}

int max_boats(vector<pair<int, int> >& boats) {
    // 起点小的那条若终点不更小，就会追上或堵在终点
    // 按起点升序、终点降序排序后，对终点求最长严格上升子序列
    sort(boats.begin(), boats.end(), cmpBoat);
    vector<int> tails;
    for (int i = 0; i < (int)boats.size(); i++) {
        int dest = boats[i].second;
        vector<int>::iterator it = lower_bound(tails.begin(), tails.end(), dest);
        if (it == tails.end()) {
            tails.push_back(dest);
        } else {
            *it = dest;
        }
    }
    return (int)tails.size();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        vector<pair<int, int> > boats(m);
        for (int i = 0; i < m; i++) {
            cin >> boats[i].first;
        }
        for (int i = 0; i < m; i++) {
            cin >> boats[i].second;
        }
        cout << max_boats(boats) << "\n";
    }
    return 0;
}
