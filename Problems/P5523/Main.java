import java.io.*;
import java.util.*;

public class Main {
    // 构造长度 L 的最大合法数
    static String maxOfLen(int L, List<Integer> digits) {
        List<Integer> nz = new ArrayList<>();
        for (int d : digits) if (d > 0) nz.add(d);
        if (L <= 0) return null;
        if (nz.isEmpty()) {
            if (L == 1 && digits.contains(0)) return "0";
            return null;
        }
        int mx = Collections.max(digits);
        int first = Collections.max(nz);
        StringBuilder sb = new StringBuilder();
        sb.append(first);
        for (int i = 1; i < L; i++) sb.append(mx);
        return sb.toString();
    }

    // 等长且严格小于 s：迭代从右往左找可减小位
    static String maxSameLenLt(String s, List<Integer> digits) {
        boolean[] has = new boolean[10];
        int mx = 0;
        for (int d : digits) {
            has[d] = true;
            mx = Math.max(mx, d);
        }
        int n = s.length();
        int[] sdig = new int[n];
        for (int i = 0; i < n; i++) sdig[i] = s.charAt(i) - '0';

        for (int i = n - 1; i >= 0; i--) {
            boolean ok = true;
            for (int j = 0; j < i; j++) {
                if (!has[sdig[j]]) { ok = false; break; }
                if (j == 0 && n > 1 && sdig[j] == 0) { ok = false; break; }
            }
            if (!ok) continue;
            int bestD = -1;
            for (int d = 0; d < sdig[i]; d++) {
                if (!has[d]) continue;
                if (i == 0 && n > 1 && d == 0) continue;
                bestD = d;
            }
            if (bestD < 0) continue;
            StringBuilder sb = new StringBuilder();
            for (int j = 0; j < i; j++) sb.append(sdig[j]);
            sb.append(bestD);
            for (int j = i + 1; j < n; j++) sb.append(mx);
            return sb.toString();
        }
        return null;
    }

    static String better(String a, String b) {
        if (a == null) return b;
        if (b == null) return a;
        if (a.length() != b.length()) return a.length() > b.length() ? a : b;
        return a.compareTo(b) >= 0 ? a : b;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String[] sp = br.readLine().trim().split("\\s+");
        Set<Integer> st = new HashSet<>();
        for (int i = 0; i < n; i++) st.add(Integer.parseInt(sp[i]));
        List<Integer> digits = new ArrayList<>(st);
        String s = br.readLine().trim();

        String best = maxSameLenLt(s, digits);
        if (s.length() > 1) {
            best = better(best, maxOfLen(s.length() - 1, digits));
        }
        if (best == null) System.out.println(-1);
        else System.out.println(best);
    }
}
