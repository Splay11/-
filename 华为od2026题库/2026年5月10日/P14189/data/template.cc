#include <bits/stdc++.h>
using namespace std;

#include "foo.cc"

// 模板只负责读取输入、调用用户实现并输出结果
static vector<long long> parseInput(const string& text) {
    string normalized = text;

    // 将逗号、括号等分隔符统一替换为空格，再用字符串流读取整数
    for (char& ch : normalized) {
        if (!isdigit(ch) && ch != '-') {
            ch = ' ';
        }
    }

    vector<long long> nums;
    stringstream ss(normalized);
    long long x;
    while (ss >> x) {
        nums.push_back(x);
    }
    return nums;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string input;
    string line;
    while (getline(cin, line)) {
        input += line;
        input += ' ';
    }

    vector<long long> nums = parseInput(input);

    long long capacity = nums[0];
    long long align = nums[1];
    long long read_index = nums[2];
    long long write_index = nums[3];
    long long pkt_size = nums[4];

    Solution solution;
    long long ans = solution.calcWriteIndex(
        capacity,
        align,
        read_index,
        write_index,
        pkt_size
    );

    cout << ans << '\n';
    return 0;
}
