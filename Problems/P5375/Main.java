import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    static final int MOD = 998244353;
    static int[] a;
    static int[] val;
    static int[] ln;
    static int[] pow3;
    static int n;

    static int[] encode(int x) {
        // 三进制去掉前导零后，先倒序再把 0 与 2 互换
        if (x == 0) {
            return new int[] {2, 1};
        }
        int v = 0;
        int len = 0;
        while (x > 0) {
            int d = x % 3;
            x /= 3;
            v = (int) ((v * 3L + (2 - d)) % MOD);
            len++;
        }
        return new int[] {v, len};
    }

    static void pull(int p) {
        // 下标大的在高位：右儿子在前，左儿子在后
        int leftLen = ln[p * 2];
        ln[p] = leftLen + ln[p * 2 + 1];
        val[p] = (int) ((val[p * 2 + 1] * (long) pow3[leftLen] + val[p * 2]) % MOD);
    }

    static void build(int p, int l, int r) {
        if (l == r) {
            int[] e = encode(a[l]);
            val[p] = e[0];
            ln[p] = e[1];
            return;
        }
        int mid = (l + r) / 2;
        build(p * 2, l, mid);
        build(p * 2 + 1, mid + 1, r);
        pull(p);
    }

    static void update(int p, int l, int r, int idx, int x) {
        if (l == r) {
            a[idx] = x;
            int[] e = encode(x);
            val[p] = e[0];
            ln[p] = e[1];
            return;
        }
        int mid = (l + r) / 2;
        if (idx <= mid) {
            update(p * 2, l, mid, idx, x);
        } else {
            update(p * 2 + 1, mid + 1, r, idx, x);
        }
        pull(p);
    }

    static int[] query(int p, int l, int r, int ql, int qr) {
        // 返回 [ql,qr] 从右到左拼接后的 (值, 位数)
        if (ql <= l && r <= qr) {
            return new int[] {val[p], ln[p]};
        }
        int mid = (l + r) / 2;
        if (qr <= mid) {
            return query(p * 2, l, mid, ql, qr);
        }
        if (ql > mid) {
            return query(p * 2 + 1, mid + 1, r, ql, qr);
        }
        int[] L = query(p * 2, l, mid, ql, qr);
        int[] R = query(p * 2 + 1, mid + 1, r, ql, qr);
        int nv = (int) ((R[0] * (long) pow3[L[1]] + L[0]) % MOD);
        return new int[] {nv, L[1] + R[1]};
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        n = Integer.parseInt(st.nextToken());
        int q = Integer.parseInt(st.nextToken());
        a = new int[n];
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) {
            a[i] = Integer.parseInt(st.nextToken());
        }
        val = new int[n * 4 + 5];
        ln = new int[n * 4 + 5];
        int mx = 20 * n + 5;
        pow3 = new int[mx];
        pow3[0] = 1;
        for (int i = 1; i < mx; i++) {
            pow3[i] = (int) (pow3[i - 1] * 3L % MOD);
        }
        build(1, 0, n - 1);
        StringBuilder out = new StringBuilder();
        for (int t = 0; t < q; t++) {
            st = new StringTokenizer(br.readLine());
            int op = Integer.parseInt(st.nextToken());
            if (op == 1) {
                int l = Integer.parseInt(st.nextToken()) - 1;
                int r = Integer.parseInt(st.nextToken()) - 1;
                out.append(query(1, 0, n - 1, l, r)[0]).append('\n');
            } else {
                int idx = Integer.parseInt(st.nextToken()) - 1;
                int x = Integer.parseInt(st.nextToken());
                update(1, 0, n - 1, idx, x);
            }
        }
        System.out.print(out.toString());
    }
}
