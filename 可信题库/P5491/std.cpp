#include <string>
using namespace std;

class Solution {
 public:
  int maxSplitProduct(string seq) {
    int n = (int)seq.size();
    int ans = 0;
    for (int k = 1; k < n; k++) {
      int prod = stoi(seq.substr(0, k)) * stoi(seq.substr(k));
      if (prod > ans) ans = prod;
    }
    return ans;
  }
};
