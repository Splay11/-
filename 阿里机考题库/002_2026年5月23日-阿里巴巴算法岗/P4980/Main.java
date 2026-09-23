import java.io.*;
import java.util.*;

public class Main {
    static ArrayList<Integer> primes = new ArrayList<>();
    static void initPrimes() {
        int N = 32000;
        boolean[] vis = new boolean[N + 1];
        Arrays.fill(vis, true);
        for (int i = 2; i <= N; i++) {
            if (!vis[i]) continue;
            primes.add(i);
            if ((long) i * i > N) continue;
            for (int j = i * i; j <= N; j += i) vis[j] = false;
        }
    }
    static ArrayList<Integer> factorize(long x) {
        ArrayList<Integer> fac = new ArrayList<>();
        for (int p : primes) {
            if ((long) p * p > x) break;
            if (x % p == 0) {
                fac.add(p);
                while (x % p == 0) x /= p;
            }
        }
        if (x > 1) fac.add((int) x);
        return fac;
    }
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int m = Integer.parseInt(st.nextToken());
        int t = Integer.parseInt(st.nextToken());
        long[] v = new long[m];
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < m; i++) v[i] = Long.parseLong(st.nextToken());
        initPrimes();
        HashMap<Integer, Integer> pidMap = new HashMap<>();
        int pc = 0;
        int[][] facIds = new int[m][];
        for (int i = 0; i < m; i++) {
            if (v[i] == 1) { facIds[i] = new int[0]; continue; }
            ArrayList<Integer> fac = factorize(v[i]);
            facIds[i] = new int[fac.size()];
            for (int j = 0; j < fac.size(); j++) {
                int p = fac.get(j);
                Integer id = pidMap.get(p);
                if (id == null) { id = pc++; pidMap.put(p, id); }
                facIds[i][j] = id;
            }
        }
        long[] vals = v.clone();
        Arrays.sort(vals);
        int nuniq = 0;
        for (int i = 0; i < m; i++)
            if (nuniq == 0 || vals[i] != vals[nuniq - 1]) vals[nuniq++] = vals[i];
        long res = -1;
        int lo = 0, hi = nuniq - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            long M = vals[mid];
            boolean ok;
            if (t == 1) {
                ok = false;
                for (long x : v) if (x <= M) { ok = true; break; }
            } else {
                int[] best = new int[pc];
                int mx = 0;
                ok = false;
                for (int i = 0; i < m; i++) {
                    if (v[i] > M || v[i] == 1) continue;
                    int dp = 1;
                    for (int id : facIds[i]) if (best[id] + 1 > dp) dp = best[id] + 1;
                    if (dp > mx) mx = dp;
                    if (mx >= t) { ok = true; break; }
                    for (int id : facIds[i]) if (best[id] < dp) best[id] = dp;
                }
            }
            if (ok) { res = M; hi = mid - 1; }
            else lo = mid + 1;
        }
        System.out.println(res);
    }
}
