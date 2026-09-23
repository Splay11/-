import java.io.*;
import java.util.*;

public class Main {
    private static String trim(String s) {
        return s == null ? "" : s.trim();
    }

    private static int[][] parseArray2d(String line) throws Exception {
        String s = trim(line);
        if (s.isEmpty() || s.charAt(0) != '[') throw new Exception("bad");
        ArrayList<int[]> rows = new ArrayList<>();
        int i = 1;
        while (true) {
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ']') {
                i++;
                break;
            }
            if (i >= s.length() || s.charAt(i) != '[') throw new Exception("bad");
            i++;
            ArrayList<Integer> row = new ArrayList<>();
            while (true) {
                while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
                if (i < s.length() && s.charAt(i) == ']') {
                    i++;
                    break;
                }
                int sign = 1;
                if (i < s.length() && s.charAt(i) == '-') {
                    sign = -1;
                    i++;
                }
                int v = 0;
                boolean ok = false;
                while (i < s.length() && Character.isDigit(s.charAt(i))) {
                    ok = true;
                    v = v * 10 + (s.charAt(i) - '0');
                    i++;
                }
                if (!ok) throw new Exception("bad");
                row.add(sign * v);
                while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
                if (i < s.length() && s.charAt(i) == ']') {
                    i++;
                    break;
                }
                if (i >= s.length() || s.charAt(i) != ',') throw new Exception("bad");
                i++;
            }
            int[] rr = new int[row.size()];
            for (int t = 0; t < row.size(); t++) rr[t] = row.get(t);
            rows.add(rr);
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ']') {
                i++;
                break;
            }
            if (i >= s.length() || s.charAt(i) != ',') throw new Exception("bad");
            i++;
        }
        return rows.toArray(new int[0][]);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line1 = br.readLine();
        String line2 = br.readLine();
        if (line1 == null || line2 == null) return;
        int[][] packages = parseArray2d(line1);
        int budget = Integer.parseInt(trim(line2));
        System.out.println(new Solution().bestBandwidth(packages, budget));
    }
}
