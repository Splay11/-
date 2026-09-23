#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    ParkingLot* obj = nullptr;
    regex init_re(R"(ParkingLot\((\d+)\))");
    regex reserve_re(R"(reserve\((-?\d+),\s*(-?\d+),\s*(-?\d+)\))");
    regex cancel_re(R"(cancel\((-?\d+)\))");
    regex spot_re(R"(spotOf\((-?\d+)\))");
    regex busy_re(R"(busyCount\((-?\d+)\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (regex_match(line, m, init_re)) {
            obj = new ParkingLot(stoi(m[1]));
            cout << "null\n";
        } else if (regex_match(line, m, reserve_re)) {
            cout << obj->reserve(stoi(m[1]), stoi(m[2]), stoi(m[3])) << "\n";
        } else if (regex_match(line, m, cancel_re)) {
            cout << (obj->cancel(stoi(m[1])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, spot_re)) {
            cout << obj->spotOf(stoi(m[1])) << "\n";
        } else if (regex_match(line, m, busy_re)) {
            cout << obj->busyCount(stoi(m[1])) << "\n";
        } else {
            return 1;
        }
    }
    return 0;
}
