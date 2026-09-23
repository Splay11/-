#include <algorithm>
#include <queue>
#include <vector>

using namespace std;

class Solution {
 public:
  vector<int> finishTimes(vector<int>& arrival, vector<int>& duration,
                          vector<int>& priority) {
    int n = (int)arrival.size();
    vector<int> rem = duration;
    vector<int> ans(n, -1);
    vector<int> order(n);
    for (int i = 0; i < n; i++) order[i] = i;
    sort(order.begin(), order.end(), [&](int a, int b) {
      if (arrival[a] != arrival[b]) return arrival[a] < arrival[b];
      return a < b;
    });
    // (-priority, index)
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> ready;
    long long time = 0;
    int i = 0;
    int cur = -1;

    while (i < n || !ready.empty() || cur != -1) {
      if (cur == -1 && ready.empty()) {
        if (i >= n) break;
        time = max(time, (long long)arrival[order[i]]);
      }
      while (i < n && arrival[order[i]] <= time) {
        int idx = order[i++];
        ready.push({-priority[idx], idx});
      }
      if (cur != -1) {
        if (!ready.empty()) {
          auto top = ready.top();
          if (make_pair(top.first, top.second) < make_pair(-priority[cur], cur)) {
            ready.push({-priority[cur], cur});
            cur = top.second;
            ready.pop();
          }
        }
      } else {
        if (ready.empty()) continue;
        cur = ready.top().second;
        ready.pop();
      }
      long long finish = time + rem[cur];
      if (i < n && arrival[order[i]] < finish) {
        rem[cur] -= (int)(arrival[order[i]] - time);
        time = arrival[order[i]];
      } else {
        time = finish;
        ans[cur] = (int)time;
        rem[cur] = 0;
        cur = -1;
      }
    }
    return ans;
  }
};
