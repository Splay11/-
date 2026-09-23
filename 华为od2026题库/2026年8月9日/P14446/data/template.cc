#include "foo.cc"
#include <iostream>
#include <string>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    // 解析输入："lights",t
    // 找到第一个引号后的内容
    size_t start = line.find('"');
    size_t end = line.find('"', start + 1);
    string lights = line.substr(start + 1, end - start - 1);

    // 逗号后的整数
    size_t comma = line.find(',', end);
    int t = stoi(line.substr(comma + 1));

    Solution solution;
    string result = solution.lightStripTransform(lights, t);
    cout << "\"" << result << "\"" << endl;
    return 0;
}
