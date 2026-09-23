#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 解析输入行：格式为 N,K,M,[a1,a2,...,aN]
int main() {
    string line;
    getline(cin, line);

    // 找到第一个逗号位置，解析 N
    int pos1 = line.find(',');
    int N = stoi(line.substr(0, pos1));

    // 找第二个逗号，解析 K
    int pos2 = line.find(',', pos1 + 1);
    int K = stoi(line.substr(pos1 + 1, pos2 - pos1 - 1));

    // 找第三个逗号（即 '[' 后的内容分隔），解析 M
    int pos3 = line.find(',', pos2 + 1);
    int M = stoi(line.substr(pos2 + 1, pos3 - pos2 - 1));

    // 解析数组部分：去除 '[' 和 ']'
    string arrStr = line.substr(pos3 + 1);
    // 格式: [a1,a2,...,aN]
    if (!arrStr.empty() && arrStr[0] == '[') {
        arrStr = arrStr.substr(1);
    }
    if (!arrStr.empty() && arrStr.back() == ']') {
        arrStr.pop_back();
    }

    vector<int> A;
    size_t start = 0, end;
    while ((end = arrStr.find(',', start)) != string::npos) {
        A.push_back(stoi(arrStr.substr(start, end - start)));
        start = end + 1;
    }
    // 最后一个元素
    if (start < arrStr.size()) {
        A.push_back(stoi(arrStr.substr(start)));
    }

    Solution solution;
    cout << solution.maxSpiritPower(N, K, M, A) << endl;
    return 0;
}
