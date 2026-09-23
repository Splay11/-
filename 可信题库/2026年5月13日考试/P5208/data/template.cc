#include "foo.cc"
#include <cctype>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

static string trim(const string& s) {
    size_t a = 0;
    while (a < s.size() && isspace((unsigned char)s[a])) a++;
    size_t b = s.size();
    while (b > a && isspace((unsigned char)s[b - 1])) b--;
    return s.substr(a, b - a);
}

static vector<int> parseIntArray(const string& s0) {
    string s = trim(s0);
    vector<int> vals;
    size_t i = 0;
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') break;
        int sign = 1;
        if (i < s.size() && s[i] == '-') {
            sign = -1;
            i++;
        }
        int v = 0;
        bool ok = false;
        while (i < s.size() && isdigit((unsigned char)s[i])) {
            ok = true;
            v = v * 10 + (s[i] - '0');
            i++;
        }
        if (!ok) exit(1);
        vals.push_back(sign * v);
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') break;
        if (i >= s.size() || s[i] != ',') exit(1);
        i++;
    }
    return vals;
}

static string fmtList(const vector<int>& a) {
    if (a.empty()) return "[]";
    string s = "[";
    for (size_t i = 0; i < a.size(); i++) {
        if (i) s += ", ";
        s += to_string(a[i]);
    }
    s += "]";
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    GCSystem* obj = nullptr;
    bool first = true;
    while (getline(cin, line)) {
        line = trim(line);
        if (line.empty()) continue;
        if (!first) cout << "\n";
        first = false;
        if (line.rfind("GCSystem(", 0) == 0) {
            int ys = stoi(line.substr(9, line.size() - 10));
            delete obj;
            obj = new GCSystem(ys);
            cout << "null";
        } else if (line.rfind("createObject(", 0) == 0) {
            int id = stoi(line.substr(13, line.size() - 14));
            obj->createObject(id);
            cout << "null";
        } else if (line.rfind("markObjects(", 0) == 0) {
            string inner = line.substr(12, line.size() - 13);
            obj->markObjects(parseIntArray(inner));
            cout << "null";
        } else if (line.rfind("manualGC(", 0) == 0) {
            int g = stoi(line.substr(9, line.size() - 10));
            obj->manualGC(g);
            cout << "null";
        } else if (line.rfind("getLiveObjects(", 0) == 0) {
            int g = stoi(line.substr(15, line.size() - 16));
            cout << fmtList(obj->getLiveObjects(g));
        } else {
            return 1;
        }
    }
    cout << "\n";
    delete obj;
    return 0;
}
