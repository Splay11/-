import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.StringTokenizer;

public class Main {
    static class FenwickMax {
        int n;
        int[] a;

        FenwickMax(int n) {
            this.n = n;
            this.a = new int[n + 1];
        }

        void upd(int i, int v) {
            while (i <= n) {
                if (v > a[i]) a[i] = v;
                i += i & -i;
            }
        }

        int qry(int i) {
            int r = 0;
            while (i > 0) {
                if (a[i] > r) r = a[i];
                i -= i & -i;
            }
            return r;
        }
    }

    static int lowerBound(List<Integer> a, int x) {
        int l = 0, r = a.size();
        while (l < r) {
            int mid = (l + r) >>> 1;
            if (a.get(mid) < x) l = mid + 1;
            else r = mid;
        }
        return l;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        int[] u = new int[m];
        int[] v = new int[m];
        int[] w = new int[m];
        List<List<Integer>> inc = new ArrayList<List<Integer>>(n + 1);
        for (int i = 0; i <= n; ++i) inc.add(new ArrayList<Integer>());
        for (int i = 0; i < m; ++i) {
            st = new StringTokenizer(br.readLine());
            u[i] = Integer.parseInt(st.nextToken());
            v[i] = Integer.parseInt(st.nextToken());
            w[i] = Integer.parseInt(st.nextToken());
            inc.get(v[i]).add(w[i]);
        }
        List<List<Integer>> comp = new ArrayList<List<Integer>>(n + 1);
        FenwickMax[] bits = new FenwickMax[n + 1];
        for (int i = 0; i <= n; ++i) comp.add(null);
        for (int i = 1; i <= n; ++i) {
            if (inc.get(i).isEmpty()) continue;
            Set<Integer> set = new HashSet<Integer>(inc.get(i));
            List<Integer> c = new ArrayList<Integer>(set);
            Collections.sort(c);
            comp.set(i, c);
            bits[i] = new FenwickMax(c.size());
        }
        int ans = 0;
        for (int i = 0; i < m; ++i) {
            int best = 1;
            if (bits[u[i]] != null) {
                int k = lowerBound(comp.get(u[i]), w[i]);
                if (k > 0) best = 1 + bits[u[i]].qry(k);
            }
            if (best > ans) ans = best;
            int pos = lowerBound(comp.get(v[i]), w[i]) + 1;
            bits[v[i]].upd(pos, best);
        }
        System.out.println(ans);
    }
}
