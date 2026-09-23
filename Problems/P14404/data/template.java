import java.io.*;
import java.util.*;

public class Main {
    private static long readLong(String s, int[] idx) {
        while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
        int sign = 1;
        if (idx[0] < s.length() && s.charAt(idx[0]) == '-') {
            sign = -1;
            idx[0]++;
        }
        long v = 0;
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
                row.add((int) readLong(s, idx));
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

    private static String formatArray(int[] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(',');
            sb.append(a[i]);
        }
        sb.append(']');
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        ArrayList<String> parts = splitTopLevel(line);
        if (parts.size() < 2) throw new RuntimeException("bad input");
        int[] idx = {0};
        int[][] sub_arrays = parseArray2d(parts.get(0), idx);
        idx[0] = 0;
        int station_capacity = (int) readLong(parts.get(1), idx);
        Solution sol = new Solution();
        System.out.println(formatArray(sol.predictGeneration(sub_arrays, station_capacity)));
    }
}
