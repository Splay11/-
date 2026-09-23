#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    ShardLeaseManager* obj = nullptr;
    regex ctor_re(R"(ShardLeaseManager\((\d+),\s*(\d+)\))");
    regex acq_re(R"(acquire\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\))");
    regex ren_re(R"(renew\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\))");
    regex rel_re(R"(release\((-?\d+),\s*(-?\d+),\s*(-?\d+)\))");
    regex own_re(R"(owner\((-?\d+),\s*(-?\d+)\))");
    regex held_re(R"(heldCount\((-?\d+),\s*(-?\d+)\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (line.rfind("ShardLeaseManager(", 0) == 0) {
            if (!regex_match(line, m, ctor_re)) return 1;
            delete obj;
            obj = new ShardLeaseManager(stoi(m[1]), stoi(m[2]));
            cout << "null\n";
        } else if (line.rfind("acquire(", 0) == 0) {
            if (!regex_match(line, m, acq_re)) return 1;
            cout << (obj->acquire(stoi(m[1]), stoi(m[2]), stoi(m[3]), stoi(m[4])) ? "true" : "false") << "\n";
        } else if (line.rfind("renew(", 0) == 0) {
            if (!regex_match(line, m, ren_re)) return 1;
            cout << (obj->renew(stoi(m[1]), stoi(m[2]), stoi(m[3]), stoi(m[4])) ? "true" : "false") << "\n";
        } else if (line.rfind("release(", 0) == 0) {
            if (!regex_match(line, m, rel_re)) return 1;
            cout << (obj->release(stoi(m[1]), stoi(m[2]), stoi(m[3])) ? "true" : "false") << "\n";
        } else if (line.rfind("owner(", 0) == 0) {
            if (!regex_match(line, m, own_re)) return 1;
            cout << obj->owner(stoi(m[1]), stoi(m[2])) << "\n";
        } else if (line.rfind("heldCount(", 0) == 0) {
            if (!regex_match(line, m, held_re)) return 1;
            cout << obj->heldCount(stoi(m[1]), stoi(m[2])) << "\n";
        } else {
            return 1;
        }
    }
    delete obj;
    return 0;
}
