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

    private static int[] parseArray1d(String s, int start) {
        int[] idx = {start};
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
            if (s.charAt(idx[0]++) != ',') throw new RuntimeException("bad");
        }
        int[] a = new int[vals.size()];
        for (int i = 0; i < vals.size(); i++) a[i] = vals.get(i);
        return a;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        int p = line.indexOf('[');
        if (p < 0) throw new RuntimeException("bad");
        int[] idx = {0};
        int n = readInt(line, idx);
        if (idx[0] >= p || line.charAt(idx[0]++) != ',') throw new RuntimeException("bad");
        int m = readInt(line, idx);
        if (idx[0] >= p || line.charAt(idx[0]++) != ',') throw new RuntimeException("bad");
        int k = readInt(line, idx);
        int[] demands = parseArray1d(line, p);
        Solution sol = new Solution();
        System.out.println(sol.maxChargingDemand(n, m, k, demands));
    }
}
