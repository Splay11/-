import java.io.*;
import java.util.*;

public class Main {
    private static int readInt(String s, int[] idx) {
        while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
        int sign = 1;
        if (idx[0] < s.length() && s.charAt(idx[0]) == '-') {
            sign = -1;
            idx[0]++;
        }
        int v = 0;
        boolean ok = false;
        while (idx[0] < s.length() && Character.isDigit(s.charAt(idx[0]))) {
            ok = true;
            v = v * 10 + (s.charAt(idx[0]++) - '0');
        }
        if (!ok) throw new RuntimeException("bad int");
        return sign * v;
    }

    private static int[] parseArray1d(String s, int[] idx) {
        while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
        if (idx[0] >= s.length() || s.charAt(idx[0]) != '[') throw new RuntimeException("bad");
        idx[0]++;
        ArrayList<Integer> vals = new ArrayList<>();
        while (true) {
            while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
            if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            vals.add(readInt(s, idx));
            while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
            if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (s.charAt(idx[0]++) != ',') throw new RuntimeException("bad comma");
        }
        int[] a = new int[vals.size()];
        for (int i = 0; i < vals.size(); i++) a[i] = vals.get(i);
        return a;
    }

    private static int[][] parsePairList(String s, int[] idx) {
        while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
        if (idx[0] >= s.length() || s.charAt(idx[0]) != '[') throw new RuntimeException("bad group");
        idx[0]++;
        ArrayList<int[]> pairs = new ArrayList<>();
        while (true) {
            while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
            if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            char c = s.charAt(idx[0]);
            if (c != '(' && c != '[') throw new RuntimeException("bad pair");
            idx[0]++;
            int u = readInt(s, idx);
            if (s.charAt(idx[0]++) != ',') throw new RuntimeException("bad pair comma");
            int v = readInt(s, idx);
            char end = s.charAt(idx[0]++);
            if ((c == '(' && end != ')') || (c == '[' && end != ']')) throw new RuntimeException("bad pair end");
            pairs.add(new int[] {u, v});
            while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
            if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (s.charAt(idx[0]++) != ',') throw new RuntimeException("bad pair list comma");
        }
        return pairs.toArray(new int[0][]);
    }

    private static ArrayList<String> splitTopLevel(String line) {
        ArrayList<String> parts = new ArrayList<>();
        int start = 0, depth = 0;
        for (int i = 0; i < line.length(); i++) {
            char ch = line.charAt(i);
            if (ch == '[') depth++;
            else if (ch == ']') depth--;
            else if (ch == ',' && depth == 0) {
                parts.add(line.substring(start, i));
                start = i + 1;
            }
        }
        parts.add(line.substring(start));
        return parts;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        ArrayList<String> parts = splitTopLevel(line);
        int[] idx = {0};
        int[] resourceCount = parseArray1d(parts.get(0), idx);
        int[][][] conflicts = new int[parts.size() - 1][][];
        for (int i = 1; i < parts.size(); i++) {
            idx[0] = 0;
            conflicts[i - 1] = parsePairList(parts.get(i), idx);
        }
        Solution sol = new Solution();
        int[] ans = sol.canIsolateWithTwoPools(resourceCount, conflicts);
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < ans.length; i++) {
            if (i > 0) sb.append(',');
            sb.append(ans[i]);
        }
        sb.append(']');
        System.out.println(sb.toString());
    }
}
