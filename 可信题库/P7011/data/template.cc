#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    CertAuthority* obj = nullptr;
    regex issue_re(R"(issue\((-?\d+),\s*(-?\d+),\s*(-?\d+)\))");
    regex rev_re(R"(revoke\((-?\d+)\))");
    regex valid_re(R"(isValid\((-?\d+),\s*(-?\d+)\))");
    regex ttl_re(R"(ttl\((-?\d+),\s*(-?\d+)\))");
    regex iss_re(R"(issuerOf\((-?\d+)\))");
    regex root_re(R"(rootOf\((-?\d+)\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (line == "CertAuthority()") {
            delete obj;
            obj = new CertAuthority();
            cout << "null\n";
        } else if (line.rfind("issue(", 0) == 0) {
            if (!regex_match(line, m, issue_re)) return 1;
            cout << (obj->issue(stoi(m[1]), stoi(m[2]), stoi(m[3])) ? "true" : "false") << "\n";
        } else if (line.rfind("revoke(", 0) == 0) {
            if (!regex_match(line, m, rev_re)) return 1;
            cout << (obj->revoke(stoi(m[1])) ? "true" : "false") << "\n";
        } else if (line.rfind("isValid(", 0) == 0) {
            if (!regex_match(line, m, valid_re)) return 1;
            cout << (obj->isValid(stoi(m[1]), stoi(m[2])) ? "true" : "false") << "\n";
        } else if (line.rfind("ttl(", 0) == 0) {
            if (!regex_match(line, m, ttl_re)) return 1;
            cout << obj->ttl(stoi(m[1]), stoi(m[2])) << "\n";
        } else if (line.rfind("issuerOf(", 0) == 0) {
            if (!regex_match(line, m, iss_re)) return 1;
            cout << obj->issuerOf(stoi(m[1])) << "\n";
        } else if (line.rfind("rootOf(", 0) == 0) {
            if (!regex_match(line, m, root_re)) return 1;
            cout << obj->rootOf(stoi(m[1])) << "\n";
        } else {
            return 1;
        }
    }
    delete obj;
    return 0;
}
