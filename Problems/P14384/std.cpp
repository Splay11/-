#include <algorithm>
#include <queue>
#include <vector>

using namespace std;

class Solution {
 public:
  int countFailedCharging(int n, vector<vector<int>>& cars) {
    struct Event {
      int time;
      int pri;
      char kind;
      int id;
      bool operator>(const Event& o) const {
        if (time != o.time) return time > o.time;
        return pri > o.pri;
      }
    };

    priority_queue<Event, vector<Event>, greater<Event>> events;
    for (int i = 0; i < (int)cars.size(); i++) {
      events.push(Event{cars[i][0], 1, 'A', i});
    }

    priority_queue<int, vector<int>, greater<int>> piles;
    for (int i = 0; i < n; i++) piles.push(0);

    vector<int> waiting;
    int failed = 0;

    while (!events.empty()) {
      int t = events.top().time;
      vector<Event> batch;
      while (!events.empty() && events.top().time == t) {
        batch.push_back(events.top());
        events.pop();
      }
      sort(batch.begin(), batch.end(),
           [](const Event& a, const Event& b) { return a.pri < b.pri; });

      for (const Event& e : batch) {
        if (e.kind == 'F')
          piles.push(t);
        else
          waiting.push_back(e.id);
      }

      while (!piles.empty() && piles.top() <= t && !waiting.empty()) {
        int car = waiting[0];
        int at = cars[car][0], ct = cars[car][1], wt = cars[car][2];
        if (t - at > wt) {
          waiting.erase(waiting.begin());
          failed++;
          continue;
        }
        piles.pop();
        int finish = t + ct;
        events.push(Event{finish, 0, 'F', 0});
        waiting.erase(waiting.begin());
      }
    }
    return failed;
  }
};
