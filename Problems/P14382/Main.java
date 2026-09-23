public class Solution {
    private String s;
    private int pos;

    private boolean isAllowed(char ch) {
        if (ch >= 'a' && ch <= 'z') return true;
        if (ch >= 'A' && ch <= 'Z') return true;
        if (ch >= '0' && ch <= '9') return true;
        return ch == '+' || ch == '-';
    }

    private boolean parseNumber(int[] out) {
        int n = s.length();
        if (pos >= n) {
            return false;
        }
        if (s.charAt(pos) == '0' && pos + 1 < n) {
            char next = s.charAt(pos + 1);
            if (next == 'x' || next == 'X') {
                pos += 2;
                int val = 0;
                boolean ok = false;
                while (pos < n) {
                    char c = s.charAt(pos);
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
                    val = val * 16 + d;
                    pos++;
                }
                if (!ok || val > 999) {
                    return false;
                }
                out[0] = val;
                return true;
            }
            if (next == 'o' || next == 'O') {
                pos += 2;
                int val = 0;
                boolean ok = false;
                while (pos < n && s.charAt(pos) >= '0' && s.charAt(pos) <= '7') {
                    ok = true;
                    val = val * 8 + (s.charAt(pos) - '0');
                    pos++;
                }
                if (!ok || val > 999) {
                    return false;
                }
                out[0] = val;
                return true;
            }
        }
        if (!Character.isDigit(s.charAt(pos))) {
            return false;
        }
        int val = 0;
        while (pos < n && Character.isDigit(s.charAt(pos))) {
            val = val * 10 + (s.charAt(pos) - '0');
            pos++;
        }
        if (val > 999) {
            return false;
        }
        out[0] = val;
        return true;
    }

    public String processExpression(String inputStr) {
        s = inputStr;
        pos = 0;
        if (s.length() > 10000) {
            return "\"NA\"";
        }
        for (int i = 0; i < s.length(); i++) {
            if (!isAllowed(s.charAt(i))) {
                return "\"NA\"";
            }
        }
        if (s.isEmpty()) {
            return "\"NA\"";
        }

        int[] num = new int[1];
        if (!parseNumber(num)) {
            return "\"NA\"";
        }
        int result = num[0];

        while (pos < s.length()) {
            char op = s.charAt(pos++);
            if (op != '+' && op != '-') {
                return "\"NA\"";
            }
            if (!parseNumber(num)) {
                return "\"NA\"";
            }
            if (op == '+') {
                result += num[0];
            } else {
                result -= num[0];
            }
        }
        if (pos != s.length()) {
            return "\"NA\"";
        }

        if (result > 255) {
            result = 255;
        } else if (result < -255) {
            result = -255;
        }

        int out = (~result) & 0xFF;
        return String.format("\"0x%02X\"", out);
    }
}
