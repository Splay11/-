#include <algorithm>
#include <climits>
#include <deque>
#include <vector>

using namespace std;

class Solution {
 public:
  vector<int> simulateTaskQueue(vector<int>& submitTimes, vector<int>& execTimes,
                                int queueCapacity, int numWorkers) {
    deque<int> queue;
    int discarded = 0;
    int lastFinish = 0;
    int m = numWorkers;

    vector<int> freeAt(m + 1, 0);
    int n = (int)submitTimes.size();
    vector<pair<int, int>> subs(n);
    for (int i = 0; i < n; i++) subs[i] = {submitTimes[i], execTimes[i]};
    sort(subs.begin(), subs.end());
    int si = 0;

    auto assign = [&](int time) {
      vector<int> idle;
      for (int i = 1; i <= m; i++)
        if (freeAt[i] <= time) idle.push_back(i);
      sort(idle.begin(), idle.end());
      for (int wid : idle) {
        if (queue.empty()) break;
        int dur = queue.front();
        queue.pop_front();
        int finish = time + dur;
        lastFinish = max(lastFinish, finish);
        freeAt[wid] = finish;
      }
    };

    const int INF = INT_MAX / 4;
    while (true) {
      vector<int> busy;
      for (int i = 1; i <= m; i++)
        if (freeAt[i] > 0) busy.push_back(freeAt[i]);
      if (si >= n && queue.empty() && busy.empty()) break;

      int nextSubmit = si < n ? subs[si].first : INF;
      int nextFree = busy.empty() ? INF : *min_element(busy.begin(), busy.end());
      int t = min(nextSubmit, nextFree);

      for (int i = 1; i <= m; i++)
        if (freeAt[i] > 0 && freeAt[i] <= t) freeAt[i] = 0;

      assign(t);

      while (si < n && subs[si].first == t) {
        int d = subs[si].second;
        if ((int)queue.size() >= queueCapacity) {
          queue.pop_front();
          discarded++;
        }
        queue.push_back(d);
        si++;
      }

      assign(t);
    }

    return {lastFinish, discarded};
  }
};
