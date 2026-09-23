#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    int maxBreachReach(int n, vector<vector<int>>& links, vector<int>& shield) {
        if (n <= 0) return 0;
        vector<vector<int>> g(n), ch(n);
        for (auto& e : links) {
            g[e[0]].push_back(e[1]);
            g[e[1]].push_back(e[0]);
        }
        vector<int> parent(n, -1);
        queue<int> q;
        q.push(0); parent[0] = -2;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : g[u]) if (parent[v] == -1) {
                parent[v] = u; ch[u].push_back(v); q.push(v);
            }
        }
        vector<array<char,2>> vis(n);
        vector<char> seen(n, 0);
        vector<pair<int,int>> st;
        st.push_back({0, 0});
        vis[0][0] = 1;
        while (!st.empty()) {
            auto [u, used] = st.back(); st.pop_back();
            seen[u] = 1;
            for (int v : ch[u]) {
                int nu;
                if (shield[u] > shield[v]) nu = used;
                else if (used == 0) nu = 1;
                else continue;
                if (!vis[v][nu]) {
                    vis[v][nu] = 1;
                    st.push_back({v, nu});
                }
            }
        }
        int ans = 0;
        for (char x : seen) if (x) ans++;
        return ans;
    }
};
