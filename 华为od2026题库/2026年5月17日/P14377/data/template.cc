#include <bits/stdc++.h>
using namespace std;

#include "foo.cc"

static pair<vector<int>, vector<int>> parseInput(const string& data) {
    // 输入格式：
    // [1, 1, 1, ...], [1, 2, 3, ...]
    // 这里把中括号、逗号等非数字字符统一替换为空格，再用字符串流读取整数
    string cleaned = data;

    for (char& ch : cleaned) {
        if (!isdigit(static_cast<unsigned char>(ch))) {
            ch = ' ';
        }
    }

    stringstream ss(cleaned);
    vector<int> values;
    int x;

    while (ss >> x) {
        values.push_back(x);
    }

    vector<int> colors(14);
    vector<int> numbers(14);

    for (int i = 0; i < 14; i++) {
        colors[i] = values[i];
    }

    for (int i = 0; i < 14; i++) {
        numbers[i] = values[i + 14];
    }

    return {colors, numbers};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string data((istreambuf_iterator<char>(cin)), istreambuf_iterator<char>());

    auto input = parseInput(data);

    Solution solution;
    long long ans = solution.countWinningHands(input.first, input.second);

    cout << ans << '\n';

    return 0;
}
