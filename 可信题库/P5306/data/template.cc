#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string line; LeaseManager* obj = nullptr;
    regex init_re(R"(LeaseManager\((-?\d+)\))");
    regex acquire_re(R"(acquire\((-?\d+),\s*(-?\d+),\s*(-?\d+)\))");
    regex renew_re(R"(renew\((-?\d+),\s*(-?\d+),\s*(-?\d+)\))");
    regex release_re(R"(release\((-?\d+),\s*(-?\d+)\))");
    regex holder_re(R"(holder\((-?\d+),\s*(-?\d+)\))");
    regex alive_re(R"(aliveCount\((-?\d+)\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (regex_match(line, m, init_re)) {
            obj = new LeaseManager(stoi(m[1]));
            cout << "null\n";
        } else if (regex_match(line, m, acquire_re)) {
            cout << (obj->acquire(stoi(m[1]), stoi(m[2]), stoi(m[3])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, renew_re)) {
            cout << (obj->renew(stoi(m[1]), stoi(m[2]), stoi(m[3])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, release_re)) {
            cout << (obj->release(stoi(m[1]), stoi(m[2])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, holder_re)) {
            cout << obj->holder(stoi(m[1]), stoi(m[2])) << "\n";
        } else if (regex_match(line, m, alive_re)) {
            cout << obj->aliveCount(stoi(m[1])) << "\n";
        } else return 1;
    }
    return 0;
}
