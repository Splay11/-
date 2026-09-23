import java.io.*;
import java.util.*;

public class Main {
    private static String parseLeadingQuotedString(String s, int[] posRef) {
        int pos = posRef[0];
        StringBuilder out = new StringBuilder();
        if (pos >= s.length() || s.charAt(pos) != '"') return out.toString();
        pos++;
        while (pos < s.length()) {
            char c = s.charAt(pos++);
            if (c == '\\') {
                if (pos < s.length()) out.append(s.charAt(pos++));
            } else if (c == '"') {
                break;
            } else {
                out.append(c);
            }
        }
        posRef[0] = pos;
        return out.toString();
    }

    private static List<String> parseStringList(String s) {
        List<String> list = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inString = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '"') {
                if (inString) {
                    list.add(cur.toString());
                    cur.setLength(0);
                }
                inString = !inString;
            } else if (inString) {
                cur.append(c);
            }
        }
        return list;
    }

    private static boolean splitTwoTopArrays(String rest, String[] outFirst, String[] outSecond) {
        int i = 0;
        while (i < rest.length() && (rest.charAt(i) == ' ' || rest.charAt(i) == '\t')) i++;
        if (i >= rest.length() || rest.charAt(i) != '[') return false;
        int depth = 0;
        boolean inStr = false;
        boolean esc = false;
        for (; i < rest.length(); i++) {
            char c = rest.charAt(i);
            if (esc) {
                esc = false;
                continue;
            }
            if (inStr) {
                if (c == '\\') {
                    esc = true;
                    continue;
                }
                if (c == '"') inStr = false;
                continue;
            }
            if (c == '"') {
                inStr = true;
                continue;
            }
            if (c == '[') depth++;
            else if (c == ']') {
                depth--;
                if (depth == 0) {
                    outFirst[0] = rest.substring(0, i + 1);
                    int j = i + 1;
                    while (j < rest.length() && (rest.charAt(j) == ' ' || rest.charAt(j) == '\t')) j++;
                    if (j >= rest.length() || rest.charAt(j) != ',') return false;
                    j++;
                    while (j < rest.length() && (rest.charAt(j) == ' ' || rest.charAt(j) == '\t')) j++;
                    outSecond[0] = rest.substring(j);
                    return true;
                }
            }
        }
        return false;
    }

    private static List<Integer> parseIntList(String s) {
        List<Integer> list = new ArrayList<>();
        int i = 0;
        while (i < s.length() && (s.charAt(i) == ' ' || s.charAt(i) == '\t')) i++;
        if (i >= s.length() || s.charAt(i) != '[') return list;
        i++;
        while (i < s.length()) {
            while (i < s.length() && (s.charAt(i) == ' ' || s.charAt(i) == '\t' || s.charAt(i) == ',')) {
                if (s.charAt(i) == ']') return list;
                i++;
            }
            if (i >= s.length() || s.charAt(i) == ']') break;
            int j = i;
            while (j < s.length() && (Character.isDigit(s.charAt(j)) || s.charAt(j) == '-')) j++;
            list.add(Integer.parseInt(s.substring(i, j)));
            i = j;
        }
        return list;
    }

    private static void printJsonStringList(List<String> v) {
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < v.size(); i++) {
            if (i > 0) sb.append(", ");
            sb.append('"');
            for (char c : v.get(i).toCharArray()) {
                if (c == '"' || c == '\\') sb.append('\\');
                sb.append(c);
            }
            sb.append('"');
        }
        sb.append(']');
        System.out.println(sb.toString());
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        int[] posRef = new int[] {0};
        while (posRef[0] < line.length() && (line.charAt(posRef[0]) == ' ' || line.charAt(posRef[0]) == '\t')) posRef[0]++;
        String target = parseLeadingQuotedString(line, posRef);
        while (posRef[0] < line.length() && (line.charAt(posRef[0]) == ' ' || line.charAt(posRef[0]) == '\t')) posRef[0]++;
        if (posRef[0] >= line.length() || line.charAt(posRef[0]) != ',') return;
        posRef[0]++;
        while (posRef[0] < line.length() && (line.charAt(posRef[0]) == ' ' || line.charAt(posRef[0]) == '\t')) posRef[0]++;
        String rest = line.substring(posRef[0]);
        String[] f = new String[1];
        String[] s2 = new String[1];
        if (!splitTwoTopArrays(rest, f, s2)) return;
        String filesStr = f[0];
        String sizesStr = s2[0];
        List<String> files = parseStringList(filesStr);
        List<Integer> sizes = parseIntList(sizesStr);
        Solution solution = new Solution();
        List<String> ans = solution.findMaxOccupiedPaths(target, files, sizes);
        printJsonStringList(ans);
    }
}
