#include <algorithm>
#include <numeric>
#include <vector>

using namespace std;

class Solution {
 public:
  int minimumLatency(vector<int>& nums, int k) {
    auto can = [&](long long limit) {
      int cnt = 1;
      long long s = 0;
      for (int x : nums) {
        if (s + x > limit) {
          cnt++;
          s = 0;
        }
        s += x;
      }
      return cnt <= k;
    };

    long long lo = *max_element(nums.begin(), nums.end());
    long long hi = accumulate(nums.begin(), nums.end(), 0LL);
    while (lo < hi) {
      long long mid = (lo + hi) / 2;
      if (can(mid))
        hi = mid;
      else
        lo = mid + 1;
    }
    return (int)lo;
  }
};
