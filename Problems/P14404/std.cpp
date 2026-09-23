#include <cmath>
#include <vector>

using namespace std;

class Solution {
 public:
  vector<int> predictGeneration(vector<vector<int>>& sub_arrays,
                                int station_capacity) {
    int n = (int)sub_arrays.size();
    if (n == 0) return {};

    vector<int> base(n), mins(n), maxs(n);
    for (int i = 0; i < n; i++) {
      maxs[i] = sub_arrays[i][0];
      mins[i] = sub_arrays[i][1];
      base[i] = sub_arrays[i][2];
    }

    long long total = 0, min_total = 0;
    for (int i = 0; i < n; i++) {
      total += base[i];
      min_total += mins[i];
    }

    vector<double> values(n);
    for (int i = 0; i < n; i++) values[i] = base[i];

    if (total > station_capacity) {
      long long need = total - station_capacity;
      long long space_sum = 0;
      for (int i = 0; i < n; i++) space_sum += base[i] - mins[i];
      if (space_sum == 0) return vector<int>(n, 0);
      for (int i = 0; i < n; i++) {
        double space = base[i] - mins[i];
        values[i] = base[i] - need * space / (double)space_sum;
      }
    } else if (total < min_total) {
      long long need = min_total - total;
      long long space_sum = 0;
      for (int i = 0; i < n; i++) space_sum += maxs[i] - base[i];
      if (space_sum == 0) return vector<int>(n, 0);
      for (int i = 0; i < n; i++) {
        double space = maxs[i] - base[i];
        values[i] = base[i] + need * space / (double)space_sum;
      }
    }

    vector<int> ans(n);
    for (int i = 0; i < n; i++) {
      ans[i] = (int)ceil(values[i] - 1e-12);
    }
    return ans;
  }
};
