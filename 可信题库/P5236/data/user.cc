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
  vector<string> transformTable(vector<Cell>& table) { return {}; }
};
