import java.io.*;
import java.util.*;

public class Main {
    private static String trim(String s) {
        return s == null ? "" : s.trim();
    }

    private static String[][] parseBoard(String line) {
        line = trim(line);
        int[] idx = {0};
        if (idx[0] >= line.length() || line.charAt(idx[0]) != '[') throw new RuntimeException("bad");
        idx[0]++;
        ArrayList<String[]> rows = new ArrayList<>();
        while (true) {
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (idx[0] < line.length() && line.charAt(idx[0]) == ',') {
                idx[0]++;
                continue;
            }
            if (idx[0] >= line.length() || line.charAt(idx[0]) != '[') throw new RuntimeException("bad row");
            idx[0]++;
            ArrayList<String> row = new ArrayList<>();
            while (true) {
                while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
                if (idx[0] < line.length() && line.charAt(idx[0]) == ']') {
                    idx[0]++;
                    break;
                }
                if (idx[0] < line.length() && line.charAt(idx[0]) == ',') {
                    idx[0]++;
                    continue;
                }
                if (idx[0] >= line.length() || line.charAt(idx[0]) != '"') throw new RuntimeException("bad cell");
                idx[0]++;
                int st = idx[0];
                while (idx[0] < line.length() && line.charAt(idx[0]) != '"') idx[0]++;
                row.add(line.substring(st, idx[0]));
                if (idx[0] < line.length()) idx[0]++;
            }
            rows.add(row.toArray(new String[0]));
        }
        return rows.toArray(new String[0][]);
    }

    private static String fmt(int[] p) {
        if (p == null || p.length < 2) return "[-1, -1]";
        return "[" + p[0] + ", " + p[1] + "]";
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1 = br.readLine();
        if (l1 == null) return;
        String l2 = br.readLine();
        if (l2 == null) l2 = "[]";
        int[] ans = new Solution().findStampPos(parseBoard(l1), parseBoard(l2));
        System.out.println(fmt(ans));
    }
}
