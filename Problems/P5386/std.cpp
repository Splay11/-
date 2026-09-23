#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

vector<string> parse_tokens(const string &line) {
    // 去掉首尾花括号，按逗号拆成权值或空位 #
    string s = line;
    if (!s.empty() && s[0] == '{') {
        s = s.substr(1);
    }
    if (!s.empty() && s.back() == '}') {
        s.pop_back();
    }
    vector<string> toks;
    if (s.empty()) {
        return toks;
    }
    stringstream ss(s);
    string item;
    while (getline(ss, item, ',')) {
        // 去掉可能的空白
        size_t a = 0;
        while (a < item.size() && item[a] == ' ') {
            a++;
        }
        size_t b = item.size();
        while (b > a && item[b - 1] == ' ') {
            b--;
        }
        toks.push_back(item.substr(a, b - a));
    }
    return toks;
}

TreeNode *build_tree(const vector<string> &toks) {
    // 层序建树：空位不入队
    if (toks.empty() || toks[0] == "#") {
        return nullptr;
    }
    TreeNode *rt = new TreeNode(stoi(toks[0]));
    queue<TreeNode *> q;
    q.push(rt);
    size_t i = 1;
    while (!q.empty() && i < toks.size()) {
        TreeNode *node = q.front();
        q.pop();
        if (i < toks.size()) {
            if (toks[i] != "#") {
                node->left = new TreeNode(stoi(toks[i]));
                q.push(node->left);
            }
            i++;
        }
        if (i < toks.size()) {
            if (toks[i] != "#") {
                node->right = new TreeNode(stoi(toks[i]));
                q.push(node->right);
            }
            i++;
        }
    }
    return rt;
}

int tree_depth(TreeNode *root) {
    // 广度优先：根到最远叶子经过的结点数
    if (root == nullptr) {
        return 0;
    }
    queue<TreeNode *> q;
    q.push(root);
    int d = 0;
    while (!q.empty()) {
        d++;
        int sz = (int)q.size();
        for (int k = 0; k < sz; k++) {
            TreeNode *node = q.front();
            q.pop();
            if (node->left) {
                q.push(node->left);
            }
            if (node->right) {
                q.push(node->right);
            }
        }
    }
    return d;
}

int solve_line(const string &line) {
    return tree_depth(build_tree(parse_tokens(line)));
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    getline(cin, line);
    cout << solve_line(line) << "\n";
    return 0;
}
