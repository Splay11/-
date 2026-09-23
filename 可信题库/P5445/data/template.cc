#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    PickupDesk* obj = nullptr;
    regex init_re(R"(PickupDesk\(\))");
    regex order_re(R"(order\((-?\d+)\))");
    regex serve_re(R"(serve\(\))");
    regex waiting_re(R"(waiting\(\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (regex_match(line, m, init_re)) {
            obj = new PickupDesk();
            cout << "null\n";
        } else if (regex_match(line, m, order_re)) {
            cout << (obj->order(stoi(m[1])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, serve_re)) {
            cout << obj->serve() << "\n";
        } else if (regex_match(line, m, waiting_re)) {
            cout << obj->waiting() << "\n";
        } else {
            return 1;
        }
    }
    delete obj;
    return 0;
}
