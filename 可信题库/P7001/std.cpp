#include <algorithm>
#include <vector>
using namespace std;

class Solution {
 public:
  int peakConcurrent(vector<int>& starts, vector<int>& ends) {
    sort(starts.begin(), starts.end());
    sort(ends.begin(), ends.end());
    int i = 0, j = 0, cur = 0, ans = 0, n = (int)starts.size();
    while (i < n) {
      if (starts[i] < ends[j]) {
        ++cur;
        if (cur > ans) ans = cur;
        ++i;
      } else {
        --cur;
        ++j;
      }
    }
    return ans;
  }
};
