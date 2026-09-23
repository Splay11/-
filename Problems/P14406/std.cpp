#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;

class Solution {
 public:
  int countProfilePairs(vector<int>& profiles, int diff) {
    if (diff == 0) {
      unordered_map<int, int> freq;
      for (int x : profiles) freq[x]++;
      int ans = 0;
      for (const auto& p : freq)
        if (p.second >= 2) ans++;
      return ans;
    }
    unordered_set<int> seen(profiles.begin(), profiles.end());
    int ans = 0;
    for (int v : seen) {
      long long nxt = (long long)v + diff;
      if (seen.count((int)nxt)) ans++;
    }
    return ans;
  }
};
