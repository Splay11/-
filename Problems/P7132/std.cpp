#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Node {
    int val;
    Node* left;
    Node* right;
    Node(int v) : val(v), left(nullptr), right(nullptr) {}
};

// 按层序（含 null）还原二叉树。空序列表示空树
Node* buildTree(const vector<string>& tokens) {
    if (tokens.empty() || tokens[0] == "null") {
        return nullptr;
    }
    Node* root = new Node(stoi(tokens[0]));
    vector<Node*> q;
    q.push_back(root);
    int i = 1;
    int idx = 0;
    while (idx < (int)q.size() && i < (int)tokens.size()) {
        Node* cur = q[idx++];
        // 先读左孩子，null 表示这个位置没有节点
        if (i < (int)tokens.size()) {
            if (tokens[i] != "null") {
                cur->left = new Node(stoi(tokens[i]));
                q.push_back(cur->left);
            }
            i++;
        }
        // 再读右孩子
        if (i < (int)tokens.size()) {
            if (tokens[i] != "null") {
                cur->right = new Node(stoi(tokens[i]));
                q.push_back(cur->right);
            }
            i++;
        }
    }
    return root;
}

// DFS + 回溯：从根走到叶子，和等于 target 就记下路径。先左后右
void dfs(Node* node, int remain, vector<int>& path, vector<vector<int>>& ans) {
    if (node == nullptr) {
        return;
    }
    path.push_back(node->val);
    remain -= node->val;
    // 叶子：没有左右孩子
    if (node->left == nullptr && node->right == nullptr) {
        if (remain == 0) {
            ans.push_back(path);
        }
    } else {
        dfs(node->left, remain, path, ans);
        dfs(node->right, remain, path, ans);
    }
    // 回溯，把当前节点从路径里拿掉
    path.pop_back();
}

vector<vector<int>> pathSum(Node* root, int target) {
    vector<vector<int>> ans;
    vector<int> path;
    // 节点值有负数，不能因为当前和已经超过就剪枝
    dfs(root, target, path, ans);
    return ans;
}

vector<vector<int>> solve(const vector<string>& tokens, int target) {
    Node* root = buildTree(tokens);
    return pathSum(root, target);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, target;
    cin >> n >> target;
    // n=0 时没有第二行，空树
    vector<string> tokens(n);
    for (int i = 0; i < n; i++) {
        cin >> tokens[i];
    }
    vector<vector<int>> paths = solve(tokens, target);
    cout << paths.size() << '\n';
    for (int i = 0; i < (int)paths.size(); i++) {
        for (int j = 0; j < (int)paths[i].size(); j++) {
            if (j) {
                cout << ' ';
            }
            cout << paths[i][j];
        }
        cout << '\n';
    }
    return 0;
}
