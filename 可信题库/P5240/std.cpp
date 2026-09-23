#include <deque>
#include <unordered_map>
#include <vector>

using namespace std;

class Solution {
 public:
  int countKeptAlarms(vector<vector<int>>& events, int window, int limit) {
    unordered_map<int, deque<int>> dq;
    int kept = 0;
    for (auto& e : events) {
      int t = e[0], typ = e[1];
      auto& q = dq[typ];
      while (!q.empty() && q.front() <= t - window && q.front() < t) {
        q.pop_front();
      }
      if ((int)q.size() < limit) {
        q.push_back(t);
        kept++;
      }
    }
    return kept;
  }
};
