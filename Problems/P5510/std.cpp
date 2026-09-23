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

bool same(TreeNode* a, TreeNode* b) {
    if (!a && !b) return true;
    if (!a || !b || a->val != b->val) return false;
    return same(a->left, b->left) && same(a->right, b->right);
}

// 判断 sub 是否为 root 的子树
bool isSubtree(TreeNode* root, TreeNode* sub) {
    if (!sub) return true;
    if (!root) return false;
    if (same(root, sub)) return true;
    return isSubtree(root->left, sub) || isSubtree(root->right, sub);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n1, n2;
    cin >> n1;
    vector<string> t1(n1);
    for (int i = 0; i < n1; i++) cin >> t1[i];
    cin >> n2;
    vector<string> t2(n2);
    for (int i = 0; i < n2; i++) cin >> t2[i];
    cout << (isSubtree(buildTree(t1), buildTree(t2)) ? "true" : "false") << '\n';
    return 0;
}
