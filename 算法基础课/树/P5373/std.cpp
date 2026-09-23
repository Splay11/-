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

void preorder(TreeNode *root, vector<int> &res) {
    // 前序：根 -> 左 -> 右
    if (root == nullptr) {
        return;
    }
    res.push_back(root->val);
    preorder(root->left, res);
    preorder(root->right, res);
}

void inorder(TreeNode *root, vector<int> &res) {
    // 中序：左 -> 根 -> 右
    if (root == nullptr) {
        return;
    }
    inorder(root->left, res);
    res.push_back(root->val);
    inorder(root->right, res);
}

void postorder(TreeNode *root, vector<int> &res) {
    // 后序：左 -> 右 -> 根
    if (root == nullptr) {
        return;
    }
    postorder(root->left, res);
    postorder(root->right, res);
    res.push_back(root->val);
}

void print_line(const vector<int> &res) {
    for (int i = 0; i < (int)res.size(); i++) {
        if (i) {
            cout << ' ';
        }
        cout << res[i];
    }
    cout << '\n';
}

int main() {
    int n;
    cin >> n;
    vector<int> tree_arr(n);
    for (int i = 0; i < n; i++) {
        cin >> tree_arr[i];
    }

    TreeNode *root = build_tree(tree_arr);

    vector<int> pre_res, in_res, post_res;
    preorder(root, pre_res);
    inorder(root, in_res);
    postorder(root, post_res);

    print_line(pre_res);
    print_line(in_res);
    print_line(post_res);
    return 0;
}
