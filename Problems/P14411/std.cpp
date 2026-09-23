#include <algorithm>
#include <vector>

using namespace std;

class Solution {
 public:
  static constexpr int INT_MIN_VAL = -2147483648;

  vector<int> analyzeSpiritPaths(TreeNode* root, int threshold) {
    if (root == nullptr) {
      return {INT_MIN_VAL, 0, 0};
    }

    int max_val = INT_MIN_VAL;
    int count = 0;
    int has_ge = 0;

    auto dfs = [&](auto&& self, TreeNode* node, long long cur_sum, bool prev_neg) -> void {
      bool is_neg = node->val < 0;
      if (is_neg && prev_neg) return;

      long long new_sum = cur_sum + node->val;
      bool is_leaf = node->left == nullptr && node->right == nullptr;
      if (is_leaf) {
        max_val = max(max_val, (int)new_sum);
        count++;
        if (new_sum >= threshold) has_ge = 1;
        return;
      }
      if (node->left) self(self, node->left, new_sum, is_neg);
      if (node->right) self(self, node->right, new_sum, is_neg);
    };

    dfs(dfs, root, 0LL, false);
    if (count == 0) max_val = INT_MIN_VAL;
    return {max_val, has_ge, count};
  }
};
