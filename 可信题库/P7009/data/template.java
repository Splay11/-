import java.io.*;
import java.util.*;

public class Main {
    private static String trim(String s) {
        return s == null ? "" : s.trim();
    }

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

    private static int[][] parseArray2d(String line) {
        line = trim(line);
        int[] idx = {0};
        if (idx[0] >= line.length() || line.charAt(idx[0]) != '[') throw new RuntimeException("bad");
        idx[0]++;
        ArrayList<int[]> rows = new ArrayList<>();
        while (true) {
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (line.charAt(idx[0]++) != '[') throw new RuntimeException("bad row");
            ArrayList<Integer> row = new ArrayList<>();
            while (true) {
                while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
                if (idx[0] < line.length() && line.charAt(idx[0]) == ']') {
                    idx[0]++;
                    break;
                }
                row.add(readInt(line, idx));
                while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
                if (idx[0] < line.length() && line.charAt(idx[0]) == ']') {
                    idx[0]++;
                    break;
                }
                if (line.charAt(idx[0]++) != ',') throw new RuntimeException("bad comma");
            }
            int[] arr = new int[row.size()];
            for (int i = 0; i < row.size(); i++) arr[i] = row.get(i);
            rows.add(arr);
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (line.charAt(idx[0]++) != ',') throw new RuntimeException("bad comma");
        }
        return rows.toArray(new int[0][]);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1 = br.readLine();
        String l2 = br.readLine();
        String l3 = br.readLine();
        String l4 = br.readLine();
        String l5 = br.readLine();
        if (l1 == null || l2 == null || l3 == null || l4 == null || l5 == null) return;
        int n = Integer.parseInt(trim(l1));
        int[][] edges = parseArray2d(l2);
        int src = Integer.parseInt(trim(l3));
        int dst = Integer.parseInt(trim(l4));
        int riskBudget = Integer.parseInt(trim(l5));
        System.out.println(new Solution().minTrustDelay(n, edges, src, dst, riskBudget));
    }
}
