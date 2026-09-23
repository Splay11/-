#include <iostream>
#include <queue>
#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x = 0, TreeNode *l = nullptr, TreeNode *r = nullptr)
        : val(x), left(l), right(r) {}
};

TreeNode *build_tree(const vector<int> &tree_arr) {
    // 空树：数组为空，或根位置为空（用 -1 表示）
    if (tree_arr.empty() || tree_arr[0] == -1) {
        return nullptr;
    }

    queue<TreeNode *> q;
    TreeNode *rt = new TreeNode(tree_arr[0]);
    q.push(rt);

    int index = 1;
    while (!q.empty() && index < (int)tree_arr.size()) {
        TreeNode *node = q.front();
        q.pop();

        // 左孩子
        if (index < (int)tree_arr.size() && tree_arr[index] != -1) {
            node->left = new TreeNode(tree_arr[index]);
            q.push(node->left);
        }
        index++;

        // 右孩子
        if (index < (int)tree_arr.size() && tree_arr[index] != -1) {
            node->right = new TreeNode(tree_arr[index]);
            q.push(node->right);
        }
        index++;
    }

    return rt;
}

vector<int> level_order(TreeNode *root) {
    // 层序：只访问非空结点
    vector<int> res;
    if (root == nullptr) {
        return res;
    }
    queue<TreeNode *> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode *node = q.front();
        q.pop();
        res.push_back(node->val);
        if (node->left != nullptr) {
            q.push(node->left);
        }
        if (node->right != nullptr) {
            q.push(node->right);
        }
    }
    return res;
}

int main() {
    int n;
    cin >> n;
    vector<int> tree_arr(n);
    for (int i = 0; i < n; i++) {
        cin >> tree_arr[i];
    }

    TreeNode *root = build_tree(tree_arr);
    vector<int> res = level_order(root);
    for (int i = 0; i < (int)res.size(); i++) {
        if (i) {
            cout << ' ';
        }
        cout << res[i];
    }
    cout << '\n';
    return 0;
}
