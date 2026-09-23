#include <algorithm>
#include <map>
#include <set>
#include <string>
#include <vector>

using namespace std;

struct Cell {
    int rowNum;
    int colNum;
    string content;
    Cell() : rowNum(0), colNum(0) {}
    Cell(int r, int c, string s) : rowNum(r), colNum(c), content(std::move(s)) {}
};

class Solution {
   public:
    vector<string> transformTable(vector<Cell>& table) {
        if (table.empty()) return {};
        set<int> rowSet;
        int C = 0;
        for (auto& cell : table) {
            rowSet.insert(cell.rowNum);
            C = max(C, cell.colNum);
        }
        vector<int> rows(rowSet.begin(), rowSet.end());
        map<int, vector<string>> grid;
        for (int r : rows) grid[r] = vector<string>(C);
        for (auto& cell : table) grid[cell.rowNum][cell.colNum - 1] = cell.content;

        int w = 3;
        for (int r : rows)
            for (auto& s : grid[r]) w = max(w, (int)s.size());

        auto pad = [&](const string& s) { return s + string(w - (int)s.size(), ' '); };
        string sep = "+";
        for (int c = 0; c < C; c++) {
            sep += string(w, '-');
            sep.push_back('+');
        }
        vector<string> lines;
        lines.push_back(sep);
        for (int r : rows) {
            string line = "|";
            for (int c = 0; c < C; c++) {
                line += pad(grid[r][c]);
                line.push_back('|');
            }
            lines.push_back(line);
        }
        lines.push_back(sep);
        return lines;
    }
};
