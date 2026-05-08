import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

public class Main {

    static boolean existsSum(int m, int s) {
        if (s % m == 0) {
            int v = s / m;
            if (v >= 0 && v <= 5) return true;
        }
        for (int k = 0; k < 5; k++) {
            for (int t = 1; t < m; t++) {
                if (k * m + t == s && k + 1 <= 5) return true;
            }
        }
        return false;
    }

    static int maxAssignableSum(int m, long n) {
        int hi = (int) Math.min(n, (long) m * 5);
        for (int s = hi; s >= 0; s--) {
            if (existsSum(m, s)) return s;
        }
        return 0;
    }

    static List<int[]> collectPatterns(int m, int best) {
        Set<String> seen = new HashSet<>();
        List<int[]> out = new ArrayList<>();
        if (best % m == 0) {
            int v = best / m;
            if (v >= 0 && v <= 5) {
                int[] pat = new int[m];
                for (int i = 0; i < m; i++) pat[i] = v;
                String key = keyOf(pat);
                if (seen.add(key)) out.add(pat);
            }
        }
        for (int k = 0; k < 5; k++) {
            for (int t = 1; t < m; t++) {
                if (k * m + t == best && k + 1 <= 5) {
                    int[] pat = new int[m];
                    int i = 0;
                    for (; i < t; i++) pat[i] = k + 1;
                    for (; i < m; i++) pat[i] = k;
                    String key = keyOf(pat);
                    if (seen.add(key)) out.add(pat);
                }
            }
        }
        return out;
    }

    static String keyOf(int[] pat) {
        int[] cp = pat.clone();
        java.util.Arrays.sort(cp);
        StringBuilder sb = new StringBuilder();
        for (int x : cp) {
            sb.append(x).append(',');
        }
        return sb.toString();
    }

    static void dfsDescLex(int m, TreeMap<Integer, Integer> cnt, List<Integer> cur, List<String> lines) {
        if (cur.size() == m) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < m; i++) {
                if (i > 0) sb.append(',');
                sb.append(cur.get(i));
            }
            lines.add(sb.toString());
            return;
        }
        for (Map.Entry<Integer, Integer> e : cnt.entrySet()) {
            int v = e.getKey();
            int c = e.getValue();
            if (c <= 0) continue;
            cnt.put(v, c - 1);
            cur.add(v);
            dfsDescLex(m, cnt, cur, lines);
            cur.remove(cur.size() - 1);
            cnt.put(v, c);
        }
    }

    static List<String> genDescLex(int m, int[] pat) {
        TreeMap<Integer, Integer> cnt = new TreeMap<>(Collections.reverseOrder());
        for (int x : pat) cnt.merge(x, 1, Integer::sum);
        List<String> lines = new ArrayList<>();
        dfsDescLex(m, cnt, new ArrayList<>(), lines);
        return lines;
    }

    static String solve(int m, long n) {
        int best = maxAssignableSum(m, n);
        long rem = n - best;
        StringBuilder sb = new StringBuilder();
        sb.append(rem);
        for (int[] p : collectPatterns(m, best)) {
            for (String ln : genDescLex(m, p)) {
                sb.append('\n').append(ln);
            }
        }
        return sb.toString();
    }

    static boolean parseInput(String line, int[] mOut, long[] nOut) {
        if (line == null) return false;
        String s = line.trim();
        if (s.isEmpty()) return false;
        int c = 0;
        for (int i = 0; i < s.length(); i++) if (s.charAt(i) == ',') c++;
        if (c != 1) return false;
        int p = s.indexOf(',');
        String a = s.substring(0, p).trim();
        String b = s.substring(p + 1).trim();
        if (a.isEmpty() || b.isEmpty()) return false;
        for (int i = 0; i < a.length(); i++) if (!Character.isDigit(a.charAt(i))) return false;
        for (int i = 0; i < b.length(); i++) if (!Character.isDigit(b.charAt(i))) return false;
        int m = Integer.parseInt(a);
        long n = Long.parseLong(b);
        if (m < 1 || n < 0) return false;
        mOut[0] = m;
        nOut[0] = n;
        return true;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        int[] mArr = new int[1];
        long[] nArr = new long[1];
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out, StandardCharsets.UTF_8));
        if (!parseInput(line, mArr, nArr)) {
            bw.write("invalid\n");
            bw.flush();
            return;
        }
        bw.write(solve(mArr[0], nArr[0]));
        bw.write('\n');
        bw.flush();
    }
}
