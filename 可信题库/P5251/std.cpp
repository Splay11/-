#include <unordered_set>
#include <vector>

using namespace std;

class Solution {
 public:
  int firstDuplicate(vector<int>& users) {
    unordered_set<int> seen;
    for (int u : users) {
      if (seen.count(u)) return u;
      seen.insert(u);
    }
    return -1;
  }
};
