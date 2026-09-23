#include <bits/stdc++.h>
#include "foo.cc"
using namespace std;

static vector<vector<char>> parseRoomArrangement(const string& text) {
    vector<vector<char>> roomArrangement;
    vector<char> row;
    for (char ch : text) {
        if (ch == '.' || ch == '#') {
            row.push_back(ch);
        } else if (ch == ']' && !row.empty()) {
            roomArrangement.push_back(row);
            row.clear();
        }
    }
    return roomArrangement;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string text;
    {
        ostringstream oss;
        oss << cin.rdbuf();
        text = oss.str();
    }

    vector<vector<char>> roomArrangement = parseRoomArrangement(text);
    Solution solution;
    int answer = solution.networkPlanning(roomArrangement);
    cout << answer;
    return 0;
}
