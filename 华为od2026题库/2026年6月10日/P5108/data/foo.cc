#include <vector>

using namespace std;

class Solution {
 public:
  vector<int> analyzeTemperatureData(vector<int>& temperatures, int k, int t) {
    int n = (int)temperatures.size();
    int max_val = temperatures[0];
    int max_idx = 0;
    for (int i = 1; i < n; i++) {
      if (temperatures[i] > max_val) {
        max_val = temperatures[i];
        max_idx = i;
      }
    }

    int count = 0;
    int best_start = -1;
    int best_end = -1;
    int best_rise = -1;

    for (int i = 0; i <= n - k; i++) {
      bool ok = true;
      for (int j = i; j < i + k - 1; j++) {
        if (temperatures[j] >= temperatures[j + 1]) {
          ok = false;
          break;
        }
      }
      if (!ok) continue;
      int rise = temperatures[i + k - 1] - temperatures[i];
      if (rise >= t) {
        count++;
        if (rise > best_rise ||
            (rise == best_rise && (best_start == -1 || i < best_start))) {
          best_rise = rise;
          best_start = i;
          best_end = i + k - 1;
        }
      }
    }

    return {max_val, max_idx, count, best_start, best_end};
  }
};
