#include <iostream>
#include <queue>
#include <string>
#include <vector>
using namespace std;

int max_depth(const string& t) {
    // 空树
    if (t == "{}") {
        return 0;
    }
    // 去掉花括号，按逗号切开层序
    vector<string> vals;
    string cur = "";
    for (int i = 1; i + 1 < (int)t.size(); i++) {
        if (t[i] == ',') {
            vals.push_back(cur);
            cur = "";
        } else {
            cur += t[i];
        }
    }
    vals.push_back(cur);
    queue<int> q;
    q.push(0);
    int idx = 1;
    int depth = 0;
    int n = (int)vals.size();
    while (!q.empty()) {
        // 当前层每个真实探头把深度加一
        depth++;
        int sz = (int)q.size();
        for (int k = 0; k < sz; k++) {
            q.pop();
            // 至多读两个孩子；末尾省略则停止
            if (idx < n) {
                if (vals[idx] != "#") {
                    q.push(idx);
                }
                idx++;
            }
            if (idx < n) {
                if (vals[idx] != "#") {
                    q.push(idx);
                }
                idx++;
            }
        }
    }
    return depth;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    string t;
    getline(cin, t);
    cout << max_depth(t) << endl;
    return 0;
}
