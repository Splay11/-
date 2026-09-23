#include <vector>

using namespace std;

class Solution {
 public:
  int longestHealthy(vector<int>& beats) {
    int best = 0, cur = 0;
    for (int x : beats) {
      if (x == 1) {
        ++cur;
        if (cur > best) best = cur;
      } else {
        cur = 0;
      }
    }
    return best;
  }
};
