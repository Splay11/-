import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {

    static class SegmentTree {
        long[] max;
        long[] lazy;
        int n;

        SegmentTree(long[] arr, int n) {
            this.n = n;
            max = new long[n * 4];
            lazy = new long[n * 4];
            build(1, 1, n, arr);
        }

        void build(int node, int l, int r, long[] arr) {
            if (l == r) {
                max[node] = arr[l];
                return;
            }
            int mid = (l + r) >> 1;
            build(node << 1, l, mid, arr);
            build(node << 1 | 1, mid + 1, r, arr);
            max[node] = Math.max(max[node << 1], max[node << 1 | 1]);
        }

        void pushDown(int node) {
            if (lazy[node] != 0) {
                long tag = lazy[node];
                max[node << 1] += tag;
                max[node << 1 | 1] += tag;
                lazy[node << 1] += tag;
                lazy[node << 1 | 1] += tag;
                lazy[node] = 0;
            }
        }

        void rangeAdd(int node, int l, int r, int ql, int qr, long val) {
            if (ql <= l && r <= qr) {
                max[node] += val;
                lazy[node] += val;
                return;
            }
            pushDown(node);
            int mid = (l + r) >> 1;
            if (ql <= mid) {
                rangeAdd(node << 1, l, mid, ql, qr, val);
            }
            if (qr > mid) {
                rangeAdd(node << 1 | 1, mid + 1, r, ql, qr, val);
            }
            max[node] = Math.max(max[node << 1], max[node << 1 | 1]);
        }

        long queryMax() {
            return max[1];
        }
    }

    static long solveCase(int n, long[] h, int[] sigma, int[] tau) {
        long[] seq = new long[n + 1];
        int[] posSigma = new int[n + 1];

        for (int i = 1; i <= n; i++) {
            seq[i] = h[sigma[i]];
            posSigma[sigma[i]] = i;
        }

        long[] pre = new long[n + 1];
        for (int i = 1; i <= n; i++) {
            pre[i] = pre[i - 1] + seq[i];
        }

        SegmentTree seg = new SegmentTree(pre, n);
        long ans = Math.max(0L, seg.queryMax());

        for (int i = 1; i <= n; i++) {
            int idx = tau[i];
            int p = posSigma[idx];
            long v = h[idx];

            seg.rangeAdd(1, 1, n, p, n, -v);
            ans = Math.max(ans, seg.queryMax());
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        StringBuilder sb = new StringBuilder();

        int T = fs.nextInt();
        while (T-- > 0) {
            int n = fs.nextInt();

            long[] h = new long[n + 1];
            int[] sigma = new int[n + 1];
            int[] tau = new int[n + 1];

            for (int i = 1; i <= n; i++) {
                h[i] = fs.nextLong();
            }
            for (int i = 1; i <= n; i++) {
                sigma[i] = fs.nextInt();
            }
            for (int i = 1; i <= n; i++) {
                tau[i] = fs.nextInt();
            }

            sb.append(solveCase(n, h, sigma, tau)).append('\n');
        }

        System.out.print(sb.toString());
    }

    static class FastScanner {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        String next() throws IOException {
            while (st == null || !st.hasMoreElements()) {
                st = new StringTokenizer(br.readLine());
            }
            return st.nextToken();
        }

        int nextInt() throws IOException {
            return Integer.parseInt(next());
        }

        long nextLong() throws IOException {
            return Long.parseLong(next());
        }
    }
}
