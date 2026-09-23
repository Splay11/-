#include <cctype>
#include <cstdio>
#include <string>

using namespace std;

class Solution {
    string s;
    size_t pos;

    bool parseNumber(int &val) {
        size_t n = s.size();
        if (pos >= n) {
            return false;
        }
        if (s[pos] == '0' && pos + 1 < n) {
            char next = s[pos + 1];
            if (next == 'x' || next == 'X') {
                pos += 2;
                int v = 0;
                bool ok = false;
                while (pos < n) {
                    char c = s[pos];
                    int d;
                    if (c >= '0' && c <= '9') {
                        d = c - '0';
                    } else if (c >= 'a' && c <= 'f') {
                        d = c - 'a' + 10;
                    } else if (c >= 'A' && c <= 'F') {
                        d = c - 'A' + 10;
                    } else {
                        break;
                    }
                    ok = true;
                    v = v * 16 + d;
                    pos++;
                }
                if (!ok || v > 999) {
                    return false;
                }
                val = v;
                return true;
            }
            if (next == 'o' || next == 'O') {
                pos += 2;
                int v = 0;
                bool ok = false;
                while (pos < n && s[pos] >= '0' && s[pos] <= '7') {
                    ok = true;
                    v = v * 8 + (s[pos] - '0');
                    pos++;
                }
                if (!ok || v > 999) {
                    return false;
                }
                val = v;
                return true;
            }
        }
        if (!isdigit((unsigned char)s[pos])) {
            return false;
        }
        int v = 0;
        while (pos < n && isdigit((unsigned char)s[pos])) {
            v = v * 10 + (s[pos] - '0');
            pos++;
        }
        if (v > 999) {
            return false;
        }
        val = v;
        return true;
    }

   public:
    string processExpression(string inputStr) {
        s = inputStr;
        pos = 0;
        if (s.size() > 10000) {
            return "\"NA\"";
        }
        for (char ch : s) {
            if (!((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z') ||
                  (ch >= '0' && ch <= '9') || ch == '+' || ch == '-')) {
                return "\"NA\"";
            }
        }
        if (s.empty()) {
            return "\"NA\"";
        }

        int val = 0;
        if (!parseNumber(val)) {
            return "\"NA\"";
        }
        int result = val;

        while (pos < s.size()) {
            char op = s[pos++];
            if (op != '+' && op != '-') {
                return "\"NA\"";
            }
            if (!parseNumber(val)) {
                return "\"NA\"";
            }
            if (op == '+') {
                result += val;
            } else {
                result -= val;
            }
        }
        if (pos != s.size()) {
            return "\"NA\"";
        }

        if (result > 255) {
            result = 255;
        } else if (result < -255) {
            result = -255;
        }

        int out = (~result) & 0xFF;
        char buf[16];
        snprintf(buf, sizeof(buf), "\"0x%02X\"", out);
        return string(buf);
    }
};
