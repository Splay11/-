#include <bits/stdc++.h>
using namespace std;

#include "foo.cc"

static vector<long long> parseNumbers(const string& text) {
    // 将除数字和负号外的字符全部替换为空格，再统一解析
    string converted = text;
    for (char& c : converted) {
        if (!isdigit(static_cast<unsigned char>(c)) && c != '-') {
            c = ' ';
        }
    }

    vector<long long> nums;
    stringstream ss(converted);
    long long x;
    while (ss >> x) {
        nums.push_back(x);
    }
    return nums;
}

static string formatResult(const vector<vector<long long>>& result) {
    // 将二维数组按题目要求格式化为紧凑输出
    stringstream out;
    out << '[';
    for (size_t i = 0; i < result.size(); ++i) {
        if (i > 0) {
            out << ',';
        }
        out << '[';
        for (size_t j = 0; j < result[i].size(); ++j) {
            if (j > 0) {
                out << ',';
            }
            out << result[i][j];
        }
        out << ']';
    }
    out << ']';
    return out.str();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 读取完整输入
    string input;
    string line;
    while (getline(cin, line)) {
        if (!input.empty()) {
            input.push_back('\n');
        }
        input += line;
    }

    if (input.find_first_not_of(" \n\r\t") == string::npos) {
        cout << "[]";
        return 0;
    }

    // 解析所有数字
    vector<long long> nums = parseNumbers(input);
    if (nums.size() < 2) {
        cout << "[]";
        return 0;
    }

    int n = static_cast<int>(nums[0]);
    int k = static_cast<int>(nums[1]);

    // 将后续数字按 [id, priority] 两两组装成 packets
    vector<vector<long long>> packets;
    packets.reserve(max(0, n));
    for (size_t i = 2; i + 1 < nums.size() && static_cast<int>(packets.size()) < n; i += 2) {
        packets.push_back({nums[i], nums[i + 1]});
    }

    // 调用用户实现的核心函数
    Solution solution;
    vector<vector<long long>> result = solution.processPackets(n, k, packets);

    // 输出结果
    cout << formatResult(result);
    return 0;
}
