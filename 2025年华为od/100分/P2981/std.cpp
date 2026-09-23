#include <algorithm>
#include <vector>

using namespace std;

class Solution {
 public:
  long long maxSolarPanelArea(vector<int>& heights) {
    int left = 0, right = (int)heights.size() - 1;
    long long best = 0;
    while (left < right) {
      long long h = min(heights[left], heights[right]);
      long long area = h * (right - left);
      if (area > best) best = area;
      if (heights[left] <= heights[right])
        left++;
      else
        right--;
    }
    return best;
  }
};
