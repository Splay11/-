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

// 按层序（含 null）还原二叉树。题目保证结果是合法 BST
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
        // 先读左孩子，null 表示没有左子树
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

// BST 反过来中序（右-根-左）就是从大到小。用栈模拟，避免链状树递归爆栈
int kthLargest(Node* root, int cnt) {
    vector<Node*> stack;
    Node* cur = root;
    while (cur != nullptr || !stack.empty()) {
        // 一路向右压栈，右边全是更大的值
        while (cur != nullptr) {
            stack.push_back(cur);
            cur = cur->right;
        }
        cur = stack.back();
        stack.pop_back();
        cnt--;
        if (cnt == 0) {
            return cur->val;
        }
        // 再转向左子树，那里全是更小的值
        cur = cur->left;
    }
    return 0;
}

int solve(const vector<string>& tokens, int cnt) {
    Node* root = buildTree(tokens);
    return kthLargest(root, cnt);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, cnt;
    cin >> n >> cnt;
    // 第二行 n 个记号：数字或 null
    vector<string> tokens(n);
    for (int i = 0; i < n; i++) {
        cin >> tokens[i];
    }
    cout << solve(tokens, cnt) << '\n';
    return 0;
}
