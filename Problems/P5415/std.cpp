#include <algorithm>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;

const string START = "Core-SW-01";

vector<string> findPath(const vector<pair<string, string>>& hops) {
    map<string, vector<string>> g;
    for (size_t i = 0; i < hops.size(); i++) {
        g[hops[i].first].push_back(hops[i].second);
    }
    for (auto& kv : g) {
        sort(kv.second.rbegin(), kv.second.rend());
    }
    vector<string> route;
    vector<string> st;
    st.push_back(START);
    while (!st.empty()) {
        string u = st.back();
        if (!g[u].empty()) {
            // 出边已按终点名字从大到小排，弹出末尾就是当前更小的终点
            // 有未用跳转就继续往前走，把终点压栈
            // 没有出边才记下当前点，相当于后序，死胡同会先出现在答案尾部
            // 这样不会像纯贪心那样走进死胡同就再也回不来
            string v = g[u].back();
            g[u].pop_back();
            st.push_back(v);
        } else {
            route.push_back(u);
            st.pop_back();
        }
    }
    reverse(route.begin(), route.end());
    return route;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    vector<pair<string, string>> hops;
    string u, v;
    while (cin >> u >> v) {
        hops.push_back(make_pair(u, v));
    }
    vector<string> ans = findPath(hops);
    for (size_t i = 0; i < ans.size(); i++) {
        if (i) {
            cout << ' ';
        }
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
