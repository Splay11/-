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
        if (!ok) throw new RuntimeException("bad");
        return sign * v;
    }

    private static int[][] parseCars(String s, int start) {
        int[] idx = {start};
        while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
        if (idx[0] >= s.length() || s.charAt(idx[0]) != '[') throw new RuntimeException("bad");
        idx[0]++;
        ArrayList<int[]> rows = new ArrayList<>();
        while (true) {
            while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
            if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (s.charAt(idx[0]) != '[') throw new RuntimeException("bad");
            idx[0]++;
            ArrayList<Integer> row = new ArrayList<>();
            while (true) {
                while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
                if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                    idx[0]++;
                    break;
                }
                row.add(readInt(s, idx));
                while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
                if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                    idx[0]++;
                    break;
                }
                if (s.charAt(idx[0]++) != ',') throw new RuntimeException("bad");
            }
            int[] a = new int[row.size()];
            for (int i = 0; i < row.size(); i++) a[i] = row.get(i);
            rows.add(a);
            while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
            if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (s.charAt(idx[0]++) != ',') throw new RuntimeException("bad");
        }
        return rows.toArray(new int[0][]);
    }

    private static Object[] parseLine(String line) {
        int[] idx = {0};
        int n = readInt(line, idx);
        if (idx[0] >= line.length() || line.charAt(idx[0]++) != ',') throw new RuntimeException("bad");
        int m = readInt(line, idx);
        if (idx[0] >= line.length() || line.charAt(idx[0]++) != ',') throw new RuntimeException("bad");
        int[][] cars = parseCars(line, idx[0]);
        return new Object[] {n, m, cars};
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        Object[] pk = parseLine(line.trim());
        int n = (Integer) pk[0];
        int[][] cars = (int[][]) pk[2];
        Solution sol = new Solution();
        System.out.println(sol.countFailedCharging(n, cars));
    }
}
