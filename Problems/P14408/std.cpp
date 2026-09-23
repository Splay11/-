#include <vector>

using namespace std;

class Solution {
 public:
  vector<vector<int>> selectMaxWeightPolicies(
      int n, int k, vector<int>& weights, vector<vector<int>>& conflicts) {
    if (k < 0 || k > n) return {};

    vector<int> conflict_mask(n, 0);
    for (const auto& e : conflicts) {
      int a = e[0] - 1;
      int b = e[1] - 1;
      conflict_mask[a] |= 1 << b;
      conflict_mask[b] |= 1 << a;
    }

    auto is_independent = [&](int mask) {
      int m = mask;
      while (m) {
        int lsb = m & -m;
        int i = __builtin_ctz(m);
        if (conflict_mask[i] & mask) return false;
        m ^= lsb;
      }
      return true;
    };

    auto popcount = [](int x) { return __builtin_popcount(x); };

    bool found = false;
    int best = 0;
    vector<vector<int>> result;
    for (int mask = 0; mask < (1 << n); mask++) {
      if (popcount(mask) != k) continue;
      if (!is_independent(mask)) continue;
      int total = 0;
      vector<int> combo;
      for (int i = 0; i < n; i++) {
        if (mask & (1 << i)) {
          total += weights[i];
          combo.push_back(i + 1);
        }
      }
      if (!found || total > best) {
        found = true;
        best = total;
        result = {combo};
      } else if (total == best) {
        result.push_back(combo);
      }
    }

    if (!found) return {};
    return result;
  }
};
