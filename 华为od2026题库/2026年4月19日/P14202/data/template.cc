#include <bits/stdc++.h>
using namespace std;

#include "foo.cc"

static string 读取输入() {
    ostringstream oss;
    oss << cin.rdbuf();
    string data = oss.str();
    while (!data.empty() && (data.back() == '\n' || data.back() == '\r' || data.back() == ' ' || data.back() == '\t')) {
        data.pop_back();
    }
    size_t start = 0;
    while (start < data.size() && (data[start] == ' ' || data[start] == '\t' || data[start] == '\n' || data[start] == '\r')) {
        start++;
    }
    data = data.substr(start);
    if (data.size() >= 2 && data.front() == '"' && data.back() == '"') {
        return data.substr(1, data.size() - 2);
    }
    return data;
}

int main() {
    string sortResolutions = 读取输入();
    Solution solution;
    string result = solution.sort(sortResolutions);
    cout << result;
    return 0;
}
