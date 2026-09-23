#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    ParcelSlots* obj = nullptr;
    regex ctor_re(R"(ParcelSlots\((-?\d+)\))");
    regex put_re(R"(put\((-?\d+),\s*(-?\d+)\))");
    regex take_re(R"(take\((-?\d+)\))");
    regex move_re(R"(moveRight\((-?\d+)\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (line.rfind("ParcelSlots(", 0) == 0) {
            if (!regex_match(line, m, ctor_re)) return 1;
            delete obj;
            obj = new ParcelSlots(stoi(m[1]));
            cout << "null\n";
        } else if (line.rfind("put(", 0) == 0) {
            if (!regex_match(line, m, put_re)) return 1;
            cout << (obj->put(stoi(m[1]), stoi(m[2])) ? "true" : "false") << "\n";
        } else if (line.rfind("take(", 0) == 0) {
            if (!regex_match(line, m, take_re)) return 1;
            cout << obj->take(stoi(m[1])) << "\n";
        } else if (line.rfind("moveRight(", 0) == 0) {
            if (!regex_match(line, m, move_re)) return 1;
            cout << (obj->moveRight(stoi(m[1])) ? "true" : "false") << "\n";
        } else if (line == "occupied()") {
            cout << obj->occupied() << "\n";
        } else {
            return 1;
        }
    }
    delete obj;
    return 0;
}
