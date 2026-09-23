#include <bits/stdc++.h>
using namespace std;

#include "foo.cc"

class Parser {
private:
    string s;
    size_t p;

    void skip() {
        while (p < s.size() && isspace((unsigned char)s[p])) {
            p++;
        }
    }

    void expect(char c) {
        skip();
        if (p >= s.size() || s[p] != c) {
            exit(0);
        }
        p++;
    }

    bool tryConsume(char c) {
        skip();
        if (p < s.size() && s[p] == c) {
            p++;
            return true;
        }
        return false;
    }

public:
    Parser(const string& input) : s(input), p(0) {}

    void consumeComma() {
        expect(',');
    }

    string parseString() {
        skip();
        expect('"');
        string res;
        while (p < s.size()) {
            char ch = s[p++];
            if (ch == '"') {
                break;
            }
            if (ch == '\\' && p < s.size()) {
                char e = s[p++];
                if (e == '"' || e == '\\' || e == '/') {
                    res.push_back(e);
                } else if (e == 'b') {
                    res.push_back('\b');
                } else if (e == 'f') {
                    res.push_back('\f');
                } else if (e == 'n') {
                    res.push_back('\n');
                } else if (e == 'r') {
                    res.push_back('\r');
                } else if (e == 't') {
                    res.push_back('\t');
                } else {
                    res.push_back(e);
                }
            } else {
                res.push_back(ch);
            }
        }
        return res;
    }

    int parseInt() {
        skip();
        int sign = 1;
        if (p < s.size() && s[p] == '-') {
            sign = -1;
            p++;
        }
        int val = 0;
        while (p < s.size() && isdigit((unsigned char)s[p])) {
            val = val * 10 + (s[p] - '0');
            p++;
        }
        return sign * val;
    }

    vector<string> parseStringArray() {
        expect('[');
        vector<string> res;
        if (tryConsume(']')) {
            return res;
        }
        while (true) {
            res.push_back(parseString());
            if (tryConsume(']')) {
                break;
            }
            expect(',');
        }
        return res;
    }

    vector<vector<string>> parse2DStringArray() {
        expect('[');
        vector<vector<string>> res;
        if (tryConsume(']')) {
            return res;
        }
        while (true) {
            res.push_back(parseStringArray());
            if (tryConsume(']')) {
                break;
            }
            expect(',');
        }
        return res;
    }
};

string escapeJson(const string& x) {
    string res;
    for (char ch : x) {
        if (ch == '"') {
            res += "\\\"";
        } else if (ch == '\\') {
            res += "\\\\";
        } else if (ch == '\b') {
            res += "\\b";
        } else if (ch == '\f') {
            res += "\\f";
        } else if (ch == '\n') {
            res += "\\n";
        } else if (ch == '\r') {
            res += "\\r";
        } else if (ch == '\t') {
            res += "\\t";
        } else {
            res.push_back(ch);
        }
    }
    return res;
}

string toJson(const vector<vector<string>>& data) {
    string res = "[";
    for (int i = 0; i < (int)data.size(); i++) {
        if (i > 0) {
            res += ",";
        }
        res += "[";
        for (int j = 0; j < (int)data[i].size(); j++) {
            if (j > 0) {
                res += ",";
            }
            res += "\"" + escapeJson(data[i][j]) + "\"";
        }
        res += "]";
    }
    res += "]";
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string input, line;
    while (getline(cin, line)) {
        input += line;
    }

    Parser parser(input);
    vector<vector<string>> nodes = parser.parse2DStringArray();
    parser.consumeComma();
    vector<vector<string>> relations = parser.parse2DStringArray();
    parser.consumeComma();
    string myId = parser.parseString();
    parser.consumeComma();
    int maxHop = parser.parseInt();

    Solution solution;
    vector<vector<string>> result = solution.queryFriends(nodes, relations, myId, maxHop);
    cout << toJson(result);
    return 0;
}
