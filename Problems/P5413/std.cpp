#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

const int MOD = 1000000007;

// 用单调栈求左右最近严格更大元素，距离超过 k 则该侧贡献为 0
int totalInterference(const vector<int>& power, int k) {
    int n = (int)power.size();

    // ngeLeft[i]：i 左侧最近且严格更大的下标；没有则为 -1
    vector<int> ngeLeft(n, -1);
    vector<int> stack;
    for (int i = 0; i < n; i++) {
        // 栈里只保留比当前值更大的候选，栈顶就是最近的那个
        while (!stack.empty() && power[stack.back()] <= power[i]) {
            stack.pop_back();
        }
        if (!stack.empty()) {
            ngeLeft[i] = stack.back();
        }
        stack.push_back(i);
    }

    // ngeRight[i]：i 右侧最近且严格更大的下标；没有则为 -1
    vector<int> ngeRight(n, -1);
    stack.clear();
    for (int i = 0; i < n; i++) {
        // 当前值能作为栈中更小元素的「右侧第一个更大」
        while (!stack.empty() && power[stack.back()] < power[i]) {
            ngeRight[stack.back()] = i;
            stack.pop_back();
        }
        stack.push_back(i);
    }

    long long ans = 0;
    for (int i = 0; i < n; i++) {
        int left = ngeLeft[i];
        // 最近更大元素必须落在长度为 k 的搜索窗口内
        if (left != -1 && i - left <= k) {
            ans = (ans + 1LL * power[i] * (i - left)) % MOD;
        }
        int right = ngeRight[i];
        if (right != -1 && right - i <= k) {
            ans = (ans + 1LL * power[i] * (right - i)) % MOD;
        }
    }
    return (int)ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 第一行：全部基站强度，n 由元素个数得到
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> power;
    int x;
    while (ss >> x) {
        power.push_back(x);
    }
    // 第二行：最多向一侧搜索的基站个数
    int k;
    cin >> k;

    cout << totalInterference(power, k) << '\n';
    return 0;
}
