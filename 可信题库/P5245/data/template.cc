#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    TTLCache* obj = nullptr;
    regex init_re(R"(TTLCache\((-?\d+)\))");
    regex put_re(R"(put\((-?\d+),\s*(-?\d+),\s*(-?\d+)\))");
    regex get_re(R"(get\((-?\d+),\s*(-?\d+)\))");
    regex purge_re(R"(purge\((-?\d+)\))");
    regex size_re(R"(size\(\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (regex_match(line, m, init_re)) {
            obj = new TTLCache(stoi(m[1]));
            cout << "null\n";
        } else if (regex_match(line, m, put_re)) {
            obj->put(stoi(m[1]), stoi(m[2]), stoi(m[3]));
            cout << "null\n";
        } else if (regex_match(line, m, get_re)) {
            cout << obj->get(stoi(m[1]), stoi(m[2])) << "\n";
        } else if (regex_match(line, m, purge_re)) {
            cout << obj->purge(stoi(m[1])) << "\n";
        } else if (regex_match(line, m, size_re)) {
            cout << obj->size() << "\n";
        } else {
            return 1;
        }
    }
    return 0;
}
