import java.io.*;
import java.util.*;

public class Main {
    static int n, m, p, q, y;
    static long[] a, b;
    static HashMap<String, Long> memo;

    static long isqrt(long x) {
        if (x <= 0) return 0;
        long r = (long) Math.sqrt(x);
        while (r > 0 && r > x / r) r--;
        while (r + 1 > 0 && (r + 1) <= x / (r + 1)) r++;
        return r;
    }

    static boolean dfs(long hp, int ma, int mb, int u3, int u4, long pend) {
        if (hp < 1) return true;
        String key = ma + "," + mb + "," + u3 + "," + u4 + "," + pend;
        Long prev = memo.get(key);
        if (prev != null && prev <= hp) return false;
        memo.put(key, hp);

        if (pend == 1) {
            for (int i = 0; i < n; i++) {
                if (((ma >> i) & 1) != 0) continue;
                if (dfs(hp, ma | (1 << i), mb, u3, u4, a[i])) return true;
            }
        }

        long mult = pend;
        for (int j = 0; j < m; j++) {
            if (((mb >> j) & 1) != 0) continue;
            long nhp;
            if (mult != 0 && b[j] > (hp - 1) / mult) nhp = 0;
            else nhp = hp - b[j] * mult;
            if (dfs(nhp, ma, mb | (1 << j), u3, u4, 1)) return true;
        }
        if (u3 == 0) {
            long dmg = hp * (long) p / q;
            if (dfs(hp - dmg, ma, mb, 1, u4, 1)) return true;
        }
        if (u4 == 0) {
            long dmg = isqrt(hp);
            if (dfs(hp - dmg, ma, mb, u3, 1, 1)) return true;
        }
        return false;
    }

    static boolean solve() {
        memo = new HashMap<>();
        long hp = 1;
        for (int i = 0; i < y; i++) hp *= 10;
        return dfs(hp, 0, 0, 0, 0, 1);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder raw = new StringBuilder();
        for (String line; (line = br.readLine()) != null; ) {
            raw.append(line).append(' ');
        }
        StringTokenizer st = new StringTokenizer(raw.toString());
        int T = Integer.parseInt(st.nextToken());
        StringBuilder sb = new StringBuilder();
        while (T-- > 0) {
            n = Integer.parseInt(st.nextToken());
            m = Integer.parseInt(st.nextToken());
            p = Integer.parseInt(st.nextToken());
            q = Integer.parseInt(st.nextToken());
            y = Integer.parseInt(st.nextToken());
            a = new long[n];
            b = new long[m];
            for (int i = 0; i < n; i++) a[i] = Long.parseLong(st.nextToken());
            for (int i = 0; i < m; i++) b[i] = Long.parseLong(st.nextToken());
            sb.append(solve() ? "Yes" : "No").append('\n');
        }
        System.out.print(sb);
    }
}
