#include <algorithm>
#include <vector>

using namespace std;

static int popcount32(int x) {
  return __builtin_popcount(static_cast<unsigned>(x));
}

class Solution {
 public:
  vector<int> processDataArray(vector<int>& data, vector<vector<int>>& operations) {
    vector<int> arr = data;
    auto sortArr = [&]() {
      sort(arr.begin(), arr.end(), [](int a, int b) {
        int ca = popcount32(a), cb = popcount32(b);
        if (ca != cb) return ca < cb;
        return a < b;
      });
    };
    sortArr();
    for (auto& op : operations) {
      int i = op[0], j = op[1];
      int a = arr[i];
      int b = (i == j) ? a : arr[j];
      int merged = a | b;
      if (i == j) {
        arr.erase(arr.begin() + i);
      } else {
        int lo = min(i, j), hi = max(i, j);
        arr.erase(arr.begin() + hi);
        arr.erase(arr.begin() + lo);
      }
      arr.push_back(merged);
      sortArr();
    }
    return arr;
  }
};
