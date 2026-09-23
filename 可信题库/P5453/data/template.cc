#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    ParkingLane* obj = nullptr;
    regex init_re(R"(ParkingLane\((-?\d+)\))");
    regex arr_re(R"(arrive\((-?\d+)\))");
    regex dep_re(R"(depart\((-?\d+)\))");
    regex admit_re(R"(admit\(\))");
    regex undo_re(R"(undo\(\))");
    regex front_re(R"(front\(\))");
    regex wait_re(R"(waiting\(\))");
    regex size_re(R"(size\(\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (regex_match(line, m, init_re)) {
            obj = new ParkingLane(stoi(m[1]));
            cout << "null\n";
        } else if (regex_match(line, m, arr_re)) {
            cout << (obj->arrive(stoi(m[1])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, admit_re)) {
            cout << (obj->admit() ? "true" : "false") << "\n";
        } else if (regex_match(line, m, dep_re)) {
            cout << obj->depart(stoi(m[1])) << "\n";
        } else if (regex_match(line, m, undo_re)) {
            cout << (obj->undo() ? "true" : "false") << "\n";
        } else if (regex_match(line, m, front_re)) {
            cout << obj->front() << "\n";
        } else if (regex_match(line, m, wait_re)) {
            cout << obj->waiting() << "\n";
        } else if (regex_match(line, m, size_re)) {
            cout << obj->size() << "\n";
        } else return 1;
    }
    return 0;
}
