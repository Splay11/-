import java.io.*;
import java.util.*;

public class Main {
    static class Parser {
        private final String s;
        private int p;

        Parser(String s) {
            this.s = s;
            this.p = 0;
        }

        private void skip() {
            while (p < s.length() && Character.isWhitespace(s.charAt(p))) {
                p++;
            }
        }

        private void expect(char c) {
            skip();
            if (p >= s.length() || s.charAt(p) != c) {
                throw new RuntimeException("输入格式错误");
            }
            p++;
        }

        private boolean tryConsume(char c) {
            skip();
            if (p < s.length() && s.charAt(p) == c) {
                p++;
                return true;
            }
            return false;
        }

        void consumeComma() {
            expect(',');
        }

        String parseString() {
            skip();
            expect('"');
            StringBuilder sb = new StringBuilder();
            while (p < s.length()) {
                char ch = s.charAt(p++);
                if (ch == '"') {
                    break;
                }
                if (ch == '\\' && p < s.length()) {
                    char e = s.charAt(p++);
                    if (e == '"' || e == '\\' || e == '/') {
                        sb.append(e);
                    } else if (e == 'b') {
                        sb.append('\b');
                    } else if (e == 'f') {
                        sb.append('\f');
                    } else if (e == 'n') {
                        sb.append('\n');
                    } else if (e == 'r') {
                        sb.append('\r');
                    } else if (e == 't') {
                        sb.append('\t');
                    } else if (e == 'u' && p + 4 <= s.length()) {
                        String hex = s.substring(p, p + 4);
                        sb.append((char) Integer.parseInt(hex, 16));
                        p += 4;
                    } else {
                        sb.append(e);
                    }
                } else {
                    sb.append(ch);
                }
            }
            return sb.toString();
        }

        int parseInt() {
            skip();
            int sign = 1;
            if (p < s.length() && s.charAt(p) == '-') {
                sign = -1;
                p++;
            }
            int val = 0;
            while (p < s.length() && Character.isDigit(s.charAt(p))) {
                val = val * 10 + (s.charAt(p) - '0');
                p++;
            }
            return sign * val;
        }

        List<String> parseStringArray() {
            expect('[');
            List<String> res = new ArrayList<>();
            if (tryConsume(']')) {
                return res;
            }
            while (true) {
                res.add(parseString());
                if (tryConsume(']')) {
                    break;
                }
                expect(',');
            }
            return res;
        }

        List<List<String>> parse2DStringArray() {
            expect('[');
            List<List<String>> res = new ArrayList<>();
            if (tryConsume(']')) {
                return res;
            }
            while (true) {
                res.add(parseStringArray());
                if (tryConsume(']')) {
                    break;
                }
                expect(',');
            }
            return res;
        }
    }

    static String escapeJson(String x) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < x.length(); i++) {
            char ch = x.charAt(i);
            if (ch == '"') {
                sb.append("\\\"");
            } else if (ch == '\\') {
                sb.append("\\\\");
            } else if (ch == '\b') {
                sb.append("\\b");
            } else if (ch == '\f') {
                sb.append("\\f");
            } else if (ch == '\n') {
                sb.append("\\n");
            } else if (ch == '\r') {
                sb.append("\\r");
            } else if (ch == '\t') {
                sb.append("\\t");
            } else {
                sb.append(ch);
            }
        }
        return sb.toString();
    }

    static String toJson(List<List<String>> data) {
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < data.size(); i++) {
            if (i > 0) {
                sb.append(',');
            }
            sb.append('[');
            List<String> row = data.get(i);
            for (int j = 0; j < row.size(); j++) {
                if (j > 0) {
                    sb.append(',');
                }
                sb.append('"').append(escapeJson(row.get(j))).append('"');
            }
            sb.append(']');
        }
        sb.append(']');
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder input = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) {
            input.append(line);
        }

        Parser parser = new Parser(input.toString());
        List<List<String>> nodes = parser.parse2DStringArray();
        parser.consumeComma();
        List<List<String>> relations = parser.parse2DStringArray();
        parser.consumeComma();
        String myId = parser.parseString();
        parser.consumeComma();
        int maxHop = parser.parseInt();

        List<List<String>> result = new Solution().queryFriends(nodes, relations, myId, maxHop);
        System.out.print(toJson(result));
    }
}
