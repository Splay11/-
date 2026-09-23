#include <bits/stdc++.h>
using namespace std;

// 去掉前导零；全零则保留单个 0
string normalize(const string& part) {
    int i = 0;
    while (i < (int)part.size() - 1 && part[i] == '0') {
        ++i;
    }
    return part.substr(i);
}

// 不能转 64 位整数：修订号可能很长；先比长度再比字典序
int compare_part(const string& a, const string& b) {
    if (a.size() != b.size()) {
        return a.size() > b.size() ? 1 : -1;
    }
    if (a != b) {
        return a > b ? 1 : -1;
    }
    return 0;
}

vector<string> split_ver(const string& s) {
    vector<string> parts;
    string cur;
    for (char c : s) {
        if (c == '.') {
            parts.push_back(normalize(cur));
            cur.clear();
        } else {
            cur.push_back(c);
        }
    }
    parts.push_back(normalize(cur));
    return parts;
}

int compare_version(const string& v1, const string& v2) {
    vector<string> p1 = split_ver(v1);
    vector<string> p2 = split_ver(v2);
    int n = max((int)p1.size(), (int)p2.size());
    for (int i = 0; i < n; ++i) {
        string a = i < (int)p1.size() ? p1[i] : "0";
        string b = i < (int)p2.size() ? p2[i] : "0";
        int c = compare_part(a, b);
        if (c != 0) {
            return c;
        }
    }
    return 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string v1, v2;
    getline(cin, v1);
    getline(cin, v2);
    cout << compare_version(v1, v2) << "\n";
    return 0;
}
