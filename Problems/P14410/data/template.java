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

    private static int[][] parseArray2d(String s, int[] idx) {
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
            if (s.charAt(idx[0]++) != '[') throw new RuntimeException("bad row");
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
                if (s.charAt(idx[0]++) != ',') throw new RuntimeException("bad comma");
            }
            int[] arr = new int[row.size()];
            for (int i = 0; i < row.size(); i++) arr[i] = row.get(i);
            rows.add(arr);
            while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
            if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (s.charAt(idx[0]++) != ',') throw new RuntimeException("bad comma");
        }
        return rows.toArray(new int[0][]);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        int[] idx = {0};
        int[][] intervals = parseArray2d(line, idx);
        Solution sol = new Solution();
        System.out.println(sol.countIsolatedIntervals(intervals));
    }
}
