import java.io.*;
import java.util.*;
public class Main {
    private static String trim(String s) { return s == null ? "" : s.trim(); }
    private static long readLong(String s, int[] idx) {
        while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
        int sign = 1;
        if (idx[0] < s.length() && s.charAt(idx[0]) == '-') { sign = -1; idx[0]++; }
        long v = 0; boolean ok = false;
        while (idx[0] < s.length() && Character.isDigit(s.charAt(idx[0]))) {
            ok = true; v = v * 10 + (s.charAt(idx[0]++) - '0');
        }
        if (!ok) throw new RuntimeException("bad int");
        return sign * v;
    }
    private static int[] parseArray1d(String line) {
        line = trim(line); int[] idx = {0};
        if (idx[0] >= line.length() || line.charAt(idx[0]) != '[') throw new RuntimeException("bad");
        idx[0]++; ArrayList<Integer> row = new ArrayList<>();
        while (true) {
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
            row.add((int) readLong(line, idx));
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
            if (line.charAt(idx[0]++) != ',') throw new RuntimeException("bad comma");
        }
        int[] a = new int[row.size()];
        for (int i = 0; i < row.size(); i++) a[i] = row.get(i);
        return a;
    }
    private static int[][] parseArray2d(String line) {
        line = trim(line); int[] idx = {0};
        if (line.charAt(idx[0]++) != '[') throw new RuntimeException("bad");
        ArrayList<int[]> rows = new ArrayList<>();
        while (true) {
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
            rows.add(parseArray1dFrom(line, idx));
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
            if (line.charAt(idx[0]++) != ',') throw new RuntimeException("bad");
        }
        return rows.toArray(new int[0][]);
    }
    private static int[] parseArray1dFrom(String line, int[] idx) {
        if (line.charAt(idx[0]++) != '[') throw new RuntimeException("bad");
        ArrayList<Integer> row = new ArrayList<>();
        while (true) {
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
            row.add((int) readLong(line, idx));
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
            if (line.charAt(idx[0]++) != ',') throw new RuntimeException("bad");
        }
        int[] a = new int[row.size()];
        for (int i = 0; i < row.size(); i++) a[i] = row.get(i);
        return a;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1=br.readLine(), l2=br.readLine(), l3=br.readLine();
        if (l1==null||l2==null||l3==null) return;
        System.out.println(new Solution().maxDropoffReach(Integer.parseInt(trim(l1)), parseArray2d(l2), parseArray1d(l3)));
    }
}
