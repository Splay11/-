#include <bits/stdc++.h>
using namespace std;

#include "foo.cc"

int 查找匹配右括号(const string& s, int 左括号位置) {
    int 深度 = 0;
    for (int i = 左括号位置; i < (int)s.size(); i++) {
        if (s[i] == '[') {
            深度++;
        } else if (s[i] == ']') {
            深度--;
            if (深度 == 0) {
                return i;
            }
        }
    }
    return (int)s.size() - 1;
}

vector<int> 解析一维数组(string 片段) {
    for (char& c : 片段) {
        if (c == '[' || c == ']' || c == ',') {
            c = ' ';
        }
    }

    stringstream ss(片段);
    vector<int> nums;
    int x;
    while (ss >> x) {
        nums.push_back(x);
    }
    return nums;
}

vector<vector<int>> 解析二维数组(const string& 片段) {
    vector<int> flat = 解析一维数组(片段);
    vector<vector<int>> pipes;

    for (int i = 0; i + 2 < (int)flat.size(); i += 3) {
        pipes.push_back({flat[i], flat[i + 1], flat[i + 2]});
    }
    return pipes;
}

void 输出数组(const vector<int>& arr) {
    cout << '[';
    for (int i = 0; i < (int)arr.size(); i++) {
        if (i > 0) {
            cout << ',';
        }
        cout << arr[i];
    }
    cout << ']';
}

int main() {
    string input((istreambuf_iterator<char>(cin)), istreambuf_iterator<char>());
    if (input.find_first_not_of(" \n\r\t") == string::npos) {
        return 0;
    }

    int 第一个逗号 = input.find(',');
    int n = stoi(input.substr(0, 第一个逗号));

    int sources左括号 = input.find('[', 第一个逗号 + 1);
    int sources右括号 = 查找匹配右括号(input, sources左括号);
    string sources片段 = input.substr(sources左括号, sources右括号 - sources左括号 + 1);

    int pipes左括号 = input.find('[', sources右括号 + 1);
    string pipes片段 = "[]";
    if (pipes左括号 != (int)string::npos) {
        int pipes右括号 = 查找匹配右括号(input, pipes左括号);
        pipes片段 = input.substr(pipes左括号, pipes右括号 - pipes左括号 + 1);
    }

    vector<int> sources = 解析一维数组(sources片段);
    vector<vector<int>> pipes = 解析二维数组(pipes片段);

    Solution solution;
    vector<int> ans = solution.findIsolatedStations(n, sources, pipes);
    输出数组(ans);
    return 0;
}
