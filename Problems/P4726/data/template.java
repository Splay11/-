import java.io.*;
import java.util.*;

public class Main {
    private static String trim(String s) {
        int a = 0, b = s.length() - 1;
        while (a <= b && Character.isWhitespace(s.charAt(a))) a++;
        while (b >= a && Character.isWhitespace(s.charAt(b))) b--;
        return s.substring(a, b + 1);
    }

    private static int[][] parseGrid2d(String s) throws Exception {
        ArrayList<int[]> rows = new ArrayList<>();
        int i = 0;
        while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
        if (i >= s.length() || s.charAt(i) != '[') throw new Exception("bad");
        i++;
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
        int[][] g = new int[rows.size()][];
        for (int t = 0; t < rows.size(); t++) g[t] = rows.get(t);
        return g;
    }

    private static Object[] parseLine(String line) throws Exception {
        String s = trim(line);
        int d = 0;
        int end = -1;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '[') d++;
            else if (c == ']') {
                d--;
                if (d == 0) {
                    end = i;
                    break;
                }
            }
        }
        if (end < 0) throw new Exception("bad");
        String gridStr = s.substring(0, end + 1);
        String tail = trim(s.substring(end + 1));
        if (tail.length() == 0 || tail.charAt(0) != ',') throw new Exception("bad");
        int k = Integer.parseInt(trim(tail.substring(1)));
        int[][] g = parseGrid2d(gridStr);
        return new Object[] {g, k};
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        Object[] pk = parseLine(line);
        int[][] grid = (int[][]) pk[0];
        int maxDiff = (Integer) pk[1];
        Solution sol = new Solution();
        long ans = sol.countHikingPaths(grid, maxDiff);
        System.out.println(ans);
    }
}
