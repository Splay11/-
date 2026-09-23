#include <algorithm>
#include <unordered_map>
#include <vector>

using namespace std;

class Solution {
 public:
  vector<int> getLoadedFileIds(vector<int>& fileIds, vector<int>& parentIds,
                               int targetId) {
    unordered_map<int, vector<int>> children;
    for (size_t i = 0; i < fileIds.size(); i++) {
      children[parentIds[i]].push_back(fileIds[i]);
    }
    vector<int> ans;
    vector<int> stack = {targetId};
    while (!stack.empty()) {
      int u = stack.back();
      stack.pop_back();
      ans.push_back(u);
      for (int v : children[u]) stack.push_back(v);
    }
    sort(ans.begin(), ans.end());
    return ans;
  }
};
