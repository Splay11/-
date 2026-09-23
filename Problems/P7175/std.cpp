#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

// 按运算符把左右两个子表达式的值合在一起
int combine(int a, char op, int b) {
    if (op == '+') {
        return a + b;
    }
    if (op == '-') {
        return a - b;
    }
    return a * b;
}

// 连续数字合成一个整数，运算符单独记下；12 必须当成十二，不能拆开
void parse(const string& expression, vector<int>& nums, vector<char>& ops) {
    int i = 0;
    int n = (int)expression.size();
    while (i < n) {
        char ch = expression[i];
        if (ch == '+' || ch == '-' || ch == '*') {
            ops.push_back(ch);
            i++;
        } else {
            int val = 0;
            while (i < n && expression[i] >= '0' && expression[i] <= '9') {
                val = val * 10 + (expression[i] - '0');
                i++;
            }
            nums.push_back(val);
        }
    }
}

// 计算 nums[left..right] 所有加括号方式；枚举最后一次运算的位置
vector<int> dfs(int left, int right, const vector<int>& nums, const vector<char>& ops,
                vector<vector<vector<int>>>& memo, vector<vector<char>>& vis) {
    if (vis[left][right]) {
        return memo[left][right];
    }
    vis[left][right] = 1;
    vector<int> res;
    if (left == right) {
        res.push_back(nums[left]);
        memo[left][right] = res;
        return res;
    }
    for (int k = left; k < right; k++) {
        vector<int> left_vals = dfs(left, k, nums, ops, memo, vis);
        vector<int> right_vals = dfs(k + 1, right, nums, ops, memo, vis);
        char op = ops[k];
        for (int i = 0; i < (int)left_vals.size(); i++) {
            for (int j = 0; j < (int)right_vals.size(); j++) {
                res.push_back(combine(left_vals[i], op, right_vals[j]));
            }
        }
    }
    memo[left][right] = res;
    return res;
}

vector<int> solve(const string& expression) {
    vector<int> nums;
    vector<char> ops;
    parse(expression, nums, ops);
    int m = (int)nums.size();
    vector<vector<vector<int>>> memo(m, vector<vector<int>>(m));
    vector<vector<char>> vis(m, vector<char>(m, 0));
    vector<int> vals = dfs(0, m - 1, nums, ops, memo, vis);
    sort(vals.begin(), vals.end());
    return vals;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string expression;
    cin >> expression;
    vector<int> vals = solve(expression);
    cout << vals.size() << '\n';
    for (int i = 0; i < (int)vals.size(); i++) {
        if (i) {
            cout << ' ';
        }
        cout << vals[i];
    }
    cout << '\n';
    return 0;
}
