#include <algorithm>
#include <climits>
#include <vector>

using namespace std;

class Solution {
 public:
  vector<int> findMaintenanceWindow(int n, int w, vector<int>& scores) {
    if (n < w) return {-1, 0};

    long long window_sum = 0;
    int zero_count = 0;
    for (int i = 0; i < w; i++) {
      window_sum += scores[i];
      if (scores[i] == 0) zero_count++;
    }

    int best_start = -1;
    long long min_sum = LLONG_MAX;
    if (zero_count == 0) {
      min_sum = window_sum;
      best_start = 0;
    }

    for (int start = 1; start <= n - w; start++) {
      int out_val = scores[start - 1];
      int in_val = scores[start + w - 1];
      window_sum += in_val - out_val;
      if (out_val == 0) zero_count--;
      if (in_val == 0) zero_count++;
      if (zero_count == 0 && window_sum < min_sum) {
        min_sum = window_sum;
        best_start = start;
      }
    }

    if (best_start == -1) return {-1, 0};
    return {best_start, (int)min_sum};
  }
};
