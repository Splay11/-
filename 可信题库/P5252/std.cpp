#include <vector>

using namespace std;

class Solution {
 public:
  int bestBandwidth(vector<vector<int>>& packages, int budget) {
    int best_bw = -1;
    int best_price = 0;
    bool found = false;
    for (auto& p : packages) {
      int bw = p[0], price = p[1];
      if (price > budget) continue;
      if (!found || bw > best_bw || (bw == best_bw && price < best_price)) {
        best_bw = bw;
        best_price = price;
        found = true;
      }
    }
    return best_bw;
  }
};
