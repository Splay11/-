#include <cctype>
#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

#include "foo.cc"

static TreeNode* buildTree(const string& treeStr) {
  string s = treeStr;
  while (!s.empty() && isspace((unsigned char)s.back())) s.pop_back();
  size_t start = 0;
  while (start < s.size() && isspace((unsigned char)s[start])) start++;
  s = s.substr(start);
  if (s == "{}" || s == "{#}") return nullptr;
  if (s.size() < 2 || s.front() != '{' || s.back() != '}') exit(1);
  string inner = s.substr(1, s.size() - 2);
  while (!inner.empty() && isspace((unsigned char)inner.front())) inner.erase(inner.begin());
  if (inner.empty() || inner == "#") return nullptr;

  vector<string> tokens;
  {
    string cur;
    for (char c : inner) {
      if (c == ',') {
        while (!cur.empty() && isspace((unsigned char)cur.front())) cur.erase(cur.begin());
        while (!cur.empty() && isspace((unsigned char)cur.back())) cur.pop_back();
        tokens.push_back(cur);
        cur.clear();
      } else {
        cur.push_back(c);
      }
    }
    while (!cur.empty() && isspace((unsigned char)cur.front())) cur.erase(cur.begin());
    while (!cur.empty() && isspace((unsigned char)cur.back())) cur.pop_back();
    tokens.push_back(cur);
  }
  if (tokens.empty() || tokens[0] == "#") return nullptr;

  TreeNode* root = new TreeNode(stoi(tokens[0]));
  queue<TreeNode*> q;
  q.push(root);
  size_t idx = 1;
  while (!q.empty() && idx < tokens.size()) {
    TreeNode* node = q.front();
    q.pop();
    if (idx < tokens.size()) {
      string t = tokens[idx++];
      if (t != "#") {
        node->left = new TreeNode(stoi(t));
        q.push(node->left);
      }
    }
    if (idx < tokens.size()) {
      string t = tokens[idx++];
      if (t != "#") {
        node->right = new TreeNode(stoi(t));
        q.push(node->right);
      }
    }
  }
  return root;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string line;
  if (!getline(cin, line)) return 0;
  while (!line.empty() && isspace((unsigned char)line.back())) line.pop_back();

  int depth = 0;
  int end = -1;
  for (int i = 0; i < (int)line.size(); i++) {
    if (line[i] == '{') depth++;
    else if (line[i] == '}') {
      depth--;
      if (depth == 0) {
        end = i;
        break;
      }
    }
  }
  if (end < 0) return 1;
  string treeStr = line.substr(0, end + 1);
  int threshold = stoi(line.substr(end + 2));

  TreeNode* root = buildTree(treeStr);
  Solution sol;
  vector<int> ans = sol.analyzeSpiritPaths(root, threshold);
  cout << "[" << ans[0] << "," << ans[1] << "," << ans[2] << "]\n";
  return 0;
}
