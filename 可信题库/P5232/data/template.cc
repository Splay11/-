#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    MemMgmtSys* obj = nullptr;
    regex init_re(R"(MemMgmtSys\((\d+)\))");
    regex alloc_re(R"(processMemAlloc\((-?\d+),\s*(-?\d+)\))");
    regex free_re(R"(processMemFree\((-?\d+)\))");
    regex query_re(R"(processMemQuery\((-?\d+)\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (regex_match(line, m, init_re)) {
            obj = new MemMgmtSys(stoi(m[1]));
            cout << "null\n";
        } else if (regex_match(line, m, alloc_re)) {
            cout << obj->processMemAlloc(stoi(m[1]), stoi(m[2])) << "\n";
        } else if (regex_match(line, m, free_re)) {
            obj->processMemFree(stoi(m[1]));
            cout << "null\n";
        } else if (regex_match(line, m, query_re)) {
            cout << obj->processMemQuery(stoi(m[1])) << "\n";
        } else {
            return 1;
        }
    }
    return 0;
}
