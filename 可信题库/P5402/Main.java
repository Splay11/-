class Solution {
    static final long P = 131L;
    static final long Q = 13331L;

    public int[] findStampPos(String[][] tray, String[][] stamp) {
        int m = tray.length, n = tray[0].length;
        int a = stamp.length, b = stamp[0].length;
        long[][] ht = build(tray);
        long[][] hs = build(stamp);
        long[] pP = pow(m, P);
        long[] pQ = pow(n, Q);
        long need = rect(hs, 0, 0, a, b, pP, pQ);
        for (int i = 0; i <= m - a; i++) {
            for (int j = 0; j <= n - b; j++) {
                if (rect(ht, i, j, a, b, pP, pQ) == need) {
                    return new int[] {i, j};
                }
            }
        }
        return new int[] {-1, -1};
    }

    private long[][] build(String[][] g) {
        int m = g.length, n = g[0].length;
        long[][] h = new long[m + 1][n + 1];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                long v = g[i][j].charAt(0) - 64;
                h[i + 1][j + 1] = h[i][j + 1] * P + h[i + 1][j] * Q - h[i][j] * P * Q + v;
            }
        }
        return h;
    }

    private long[] pow(int k, long base) {
        long[] a = new long[k + 1];
        a[0] = 1;
        for (int i = 1; i <= k; i++) a[i] = a[i - 1] * base;
        return a;
    }

    private long rect(long[][] h, int r, int c, int a, int b, long[] pP, long[] pQ) {
        long v = h[r + a][c + b];
        v -= h[r][c + b] * pP[a];
        v -= h[r + a][c] * pQ[b];
        v += h[r][c] * pP[a] * pQ[b];
        return v;
    }
}
