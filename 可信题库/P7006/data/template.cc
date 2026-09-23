#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    ClusterPool* obj = nullptr;
    regex add_re(R"(addNode\((-?\d+),\s*(-?\d+)\))");
    regex rem_re(R"(removeNode\((-?\d+)\))");
    regex sub_re(R"(submit\((-?\d+),\s*(-?\d+)\))");
    regex kill_re(R"(kill\((-?\d+)\))");
    regex used_re(R"(usedOf\((-?\d+)\))");
    regex free_re(R"(freeOf\((-?\d+)\))");
    regex job_re(R"(jobNode\((-?\d+)\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (line == "ClusterPool()") {
            delete obj;
            obj = new ClusterPool();
            cout << "null\n";
        } else if (line.rfind("addNode(", 0) == 0) {
            if (!regex_match(line, m, add_re)) return 1;
            cout << (obj->addNode(stoi(m[1]), stoi(m[2])) ? "true" : "false") << "\n";
        } else if (line.rfind("removeNode(", 0) == 0) {
            if (!regex_match(line, m, rem_re)) return 1;
            cout << (obj->removeNode(stoi(m[1])) ? "true" : "false") << "\n";
        } else if (line.rfind("submit(", 0) == 0) {
            if (!regex_match(line, m, sub_re)) return 1;
            cout << obj->submit(stoi(m[1]), stoi(m[2])) << "\n";
        } else if (line.rfind("kill(", 0) == 0) {
            if (!regex_match(line, m, kill_re)) return 1;
            cout << (obj->kill(stoi(m[1])) ? "true" : "false") << "\n";
        } else if (line.rfind("usedOf(", 0) == 0) {
            if (!regex_match(line, m, used_re)) return 1;
            cout << obj->usedOf(stoi(m[1])) << "\n";
        } else if (line.rfind("freeOf(", 0) == 0) {
            if (!regex_match(line, m, free_re)) return 1;
            cout << obj->freeOf(stoi(m[1])) << "\n";
        } else if (line.rfind("jobNode(", 0) == 0) {
            if (!regex_match(line, m, job_re)) return 1;
            cout << obj->jobNode(stoi(m[1])) << "\n";
        } else {
            return 1;
        }
    }
    delete obj;
    return 0;
}
