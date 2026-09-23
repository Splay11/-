#include <algorithm>
#include <vector>

using namespace std;

class Solution {
 public:
  long long minimizeRangeSum(int n, vector<int>& nums) {
    vector<int> a = nums;
    sort(a.begin(), a.end());
    if (n == 2) return 0;
    long long ans = (long long)a[n - 1] - a[0];
    for (int i = 0; i < n - 1; i++) {
      long long cost = (long long)(a[i] - a[0]) + (a[n - 1] - a[i + 1]);
      if (cost < ans) ans = cost;
    }
    return ans;
  }
};
