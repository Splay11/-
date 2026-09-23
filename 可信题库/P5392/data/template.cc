#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    FileLockBoard* obj = nullptr;
    regex init_re(R"(FileLockBoard\(\))");
    regex lock_re(R"(lock\((-?\d+),\s*(-?\d+)\))");
    regex unlock_re(R"(unlock\((-?\d+),\s*(-?\d+)\))");
    regex holder_re(R"(holder\((-?\d+)\))");
    regex cnt_re(R"(lockedCount\(\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (regex_match(line, m, init_re)) {
            obj = new FileLockBoard();
            cout << "null\n";
        } else if (regex_match(line, m, lock_re)) {
            cout << (obj->lock(stoi(m[1]), stoi(m[2])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, unlock_re)) {
            cout << (obj->unlock(stoi(m[1]), stoi(m[2])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, holder_re)) {
            cout << obj->holder(stoi(m[1])) << "\n";
        } else if (regex_match(line, m, cnt_re)) {
            cout << obj->lockedCount() << "\n";
        } else {
            return 1;
        }
    }
    delete obj;
    return 0;
}
