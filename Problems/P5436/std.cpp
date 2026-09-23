#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <string>
#include <utility>
#include <vector>
using namespace std;

// 扫描线求最少卡数，以及占用等于最大值的时长之和
pair<long long, long long> minCardsAndFullLoad(const vector<pair<int, int> >& segs) {
    vector<pair<int, int> > events;
    events.reserve(segs.size() * 2);
    for (size_t i = 0; i < segs.size(); i++) {
        int beg = segs[i].first;
        int fin = segs[i].second;
        events.push_back(make_pair(beg, 1));
        events.push_back(make_pair(fin, -1));
    }
    sort(events.begin(), events.end());  // 时刻升序；delta -1 在 +1 前

    int cur = 0;
    int mx = 0;
    for (size_t i = 0; i < events.size(); i++) {
        cur += events[i].second;
        if (cur > mx) {
            mx = cur;
        }
    }

    cur = 0;
    long long total = 0;
    bool hasLast = false;
    int last = 0;
    size_t i = 0;
    while (i < events.size()) {
        int t = events[i].first;
        if (hasLast && cur == mx) {
            total += (long long)t - last;
        }
        while (i < events.size() && events[i].first == t) {
            cur += events[i].second;
            i++;
        }
        last = t;
        hasLast = true;
    }
    return make_pair(mx, total);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m;
    cin >> m;
    vector<pair<int, int> > segs;
    segs.reserve(m);
    for (int i = 0; i < m; i++) {
        string line;
        cin >> line;
        string::size_type pos = line.find(',');
        int fin = atoi(line.c_str());
        int beg = atoi(line.c_str() + pos + 1);
        segs.push_back(make_pair(beg, fin));
    }
    pair<long long, long long> ans = minCardsAndFullLoad(segs);
    cout << ans.first << '\n' << ans.second << '\n';
    return 0;
}
