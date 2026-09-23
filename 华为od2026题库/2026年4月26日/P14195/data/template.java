import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class Main {
    private static void skipWs(String s, int[] p) {
        while (p[0] < s.length() && Character.isWhitespace(s.charAt(p[0]))) p[0]++;
    }

    private static void expect(String s, int[] p, char c) {
        skipWs(s, p);
        if (p[0] >= s.length() || s.charAt(p[0]) != c) {
            throw new IllegalArgumentException("parse");
        }
        p[0]++;
    }

    private static String readString(String s, int[] p) {
        skipWs(s, p);
        expect(s, p, '"');
        StringBuilder sb = new StringBuilder();
        while (p[0] < s.length() && s.charAt(p[0]) != '"') {
            if (s.charAt(p[0]) == '\\' && p[0] + 1 < s.length()) p[0]++;
            sb.append(s.charAt(p[0]++));
        }
        expect(s, p, '"');
        return sb.toString();
    }

    private static List<String> parseStringArray(String t) {
        int[] p = new int[] {0};
        skipWs(t, p);
        expect(t, p, '[');
        List<String> out = new ArrayList<>();
        while (true) {
            skipWs(t, p);
            if (p[0] < t.length() && t.charAt(p[0]) == ']') {
                p[0]++;
                break;
            }
            out.add(readString(t, p));
            skipWs(t, p);
            if (p[0] < t.length() && t.charAt(p[0]) == ',') {
                p[0]++;
                continue;
            }
            if (p[0] < t.length() && t.charAt(p[0]) == ']') {
                p[0]++;
                break;
            }
            throw new IllegalArgumentException("parse arr");
        }
        return out;
    }

    private static List<List<String>> parsePairArray(String t) {
        int[] p = new int[] {0};
        skipWs(t, p);
        expect(t, p, '[');
        List<List<String>> out = new ArrayList<>();
        while (true) {
            skipWs(t, p);
            if (p[0] < t.length() && t.charAt(p[0]) == ']') {
                p[0]++;
                break;
            }
            expect(t, p, '[');
            String a = readString(t, p);
            skipWs(t, p);
            expect(t, p, ',');
            String b = readString(t, p);
            skipWs(t, p);
            expect(t, p, ']');
            List<String> pair = new ArrayList<>();
            pair.add(a);
            pair.add(b);
            out.add(pair);
            skipWs(t, p);
            if (p[0] < t.length() && t.charAt(p[0]) == ',') {
                p[0]++;
                continue;
            }
            if (p[0] < t.length() && t.charAt(p[0]) == ']') {
                p[0]++;
                break;
            }
            throw new IllegalArgumentException("parse pairs");
        }
        return out;
    }

    private static String[] splitTwoTopLevelArrays(String line) {
        String s = line.trim();
        int i = 0;
        while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
        if (i >= s.length() || s.charAt(i) != '[') throw new IllegalArgumentException("start");
        int depth = 0;
        int start = i;
        for (; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '[') depth++;
            else if (c == ']') {
                depth--;
                if (depth == 0) {
                    String first = s.substring(start, i + 1);
                    i++;
                    while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
                    if (i < s.length() && s.charAt(i) == ',') i++;
                    while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
                    String second = s.substring(i).trim();
                    return new String[] {first, second};
                }
            }
        }
        throw new IllegalArgumentException("split");
    }

    private static String jsonEscape(String x) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < x.length(); i++) {
            char c = x.charAt(i);
            if (c == '\\' || c == '"') sb.append('\\');
            sb.append(c);
        }
        return sb.toString();
    }

    private static void printAns(List<String> ans) {
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) sb.append(',');
            sb.append('"');
            sb.append(jsonEscape(ans.get(i)));
            sb.append('"');
        }
        sb.append(']');
        System.out.println(sb.toString());
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        if (line.isEmpty()) return;
        String[] parts = splitTwoTopLevelArrays(line);
        List<String> modules = parseStringArray(parts[0]);
        List<List<String>> dependencies = parsePairArray(parts[1]);
        Solution sol = new Solution();
        List<String> ans = sol.allBuildOrders(modules, dependencies);
        printAns(ans);
    }
}
