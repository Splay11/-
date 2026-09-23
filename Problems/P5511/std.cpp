#include <iostream>
#include <queue>
#include <string>
#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {}
};

TreeNode* buildTree(const vector<string>& tokens) {
    if (tokens.empty() || tokens[0] == "null") return nullptr;
    TreeNode* root = new TreeNode(stoi(tokens[0]));
    queue<TreeNode*> q;
    q.push(root);
    size_t i = 1;
    while (!q.empty() && i < tokens.size()) {
        TreeNode* node = q.front();
        q.pop();
        if (i < tokens.size()) {
            if (tokens[i] != "null") {
                node->left = new TreeNode(stoi(tokens[i]));
                q.push(node->left);
            }
            i++;
        }
        if (i < tokens.size()) {
            if (tokens[i] != "null") {
                node->right = new TreeNode(stoi(tokens[i]));
                q.push(node->right);
            }
            i++;
        }
    }
    return root;
}

// 层序编号法求最大宽度，每层相对归零防溢出
int widthOfBinaryTree(TreeNode* root) {
    if (!root) return 0;
    queue<pair<TreeNode*, unsigned long long>> q;
    q.push({root, 0});
    int ans = 0;
    while (!q.empty()) {
        int size = (int)q.size();
        unsigned long long left = q.front().second;
        unsigned long long right = left;
        for (int i = 0; i < size; i++) {
            TreeNode* node = q.front().first;
            unsigned long long idx = q.front().second;
            q.pop();
            idx -= left;
            right = idx;
            if (node->left) q.push({node->left, idx * 2});
            if (node->right) q.push({node->right, idx * 2 + 1});
        }
        ans = max(ans, (int)(right + 1));
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    vector<string> tokens;
    string s;
    while (cin >> s) tokens.push_back(s);
    cout << widthOfBinaryTree(buildTree(tokens)) << '\n';
    return 0;
}
