#include <bits/stdc++.h>
using namespace std;

int n, m;
vector<string> grid;
vector<vector<bool>> isSpecial;
vector<array<pair<int,int>,3>> allPositions;
unordered_set<string> finalStates;

string stateToKey(const vector<vector<bool>>& state) {
    string key;
    key.reserve(n * m);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            key.push_back(state[i][j] ? '1' : '0');
        }
    }
    return key;
}

bool canPlaceBlock(const vector<vector<bool>>& state, const array<pair<int,int>,3>& pos) {
    // 边界由预生成保证，这里仅检查占用
    for (int k = 0; k < 3; ++k) {
        int r = pos[k].first, c = pos[k].second;
        if (state[r][c]) return false;
    }
    // 至少一个端点与特殊格子重合（端点为第一个和最后一个格子）
    auto [r1, c1] = pos[0];
    auto [r3, c3] = pos[2];
    bool hasSpecialEndpoint = isSpecial[r1][c1] || isSpecial[r3][c3];
    return hasSpecialEndpoint;
}

vector<vector<bool>> placeBlock(const vector<vector<bool>>& state, const array<pair<int,int>,3>& pos) {
    vector<vector<bool>> ns = state;
    for (int k = 0; k < 3; ++k) {
        int r = pos[k].first, c = pos[k].second;
        ns[r][c] = true;
    }
    return ns;
}

void dfs(const vector<vector<bool>>& state) {
    bool canPlaceAny = false;
    for (const auto& pos : allPositions) {
        if (canPlaceBlock(state, pos)) {
            canPlaceAny = true;
            auto ns = placeBlock(state, pos);
            dfs(ns);
        }
    }
    if (!canPlaceAny) {
        finalStates.insert(stateToKey(state));
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> n >> m)) return 0;
    grid.resize(n);
    isSpecial.assign(n, vector<bool>(m, false));
    for (int i = 0; i < n; ++i) {
        cin >> grid[i];
        for (int j = 0; j < m; ++j) {
            if (grid[i][j] == '*') isSpecial[i][j] = true;
        }
    }

    // 生成所有 1x3（横向）与 3x1（纵向）位置
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j + 2 < m; ++j) {
            allPositions.push_back({ { {i,j}, {i,j+1}, {i,j+2} } });
        }
    }
    for (int i = 0; i + 2 < n; ++i) {
        for (int j = 0; j < m; ++j) {
            allPositions.push_back({ { {i,j}, {i+1,j}, {i+2,j} } });
        }
    }

    vector<vector<bool>> initialState(n, vector<bool>(m, false));
    dfs(initialState);

    cout << finalStates.size() << "\n";
    return 0;
}
