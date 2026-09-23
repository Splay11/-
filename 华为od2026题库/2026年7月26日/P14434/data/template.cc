#include "foo.cc"
#include <iostream>
#include <string>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    int i = 0, n = (int)line.size();

    // 跳过首部空白
    while (i < n && line[i] != '"') i++;
    i++; // 跳过起始引号
    string num;
    while (i < n && line[i] != '"') num += line[i++];
    i++; // 跳过结束引号

    // 解析 sourceDigits
    while (i < n && line[i] != '"') i++;
    i++;
    string sourceDigits;
    while (i < n && line[i] != '"') sourceDigits += line[i++];
    i++;

    // 解析 targetDigits
    while (i < n && line[i] != '"') i++;
    i++;
    string targetDigits;
    while (i < n && line[i] != '"') targetDigits += line[i++];

    Solution solution;
    cout << '"' << solution.convertNumber(num, sourceDigits, targetDigits) << '"' << endl;
    return 0;
}
