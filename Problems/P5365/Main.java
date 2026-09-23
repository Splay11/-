import java.io.BufferedInputStream;
import java.io.IOException;
import java.util.Arrays;

public class Main {
    static final int MAXN = 200000 + 5;
    static final int BUF = 1 << 16;
    static byte[] inbuf = new byte[BUF];
    static int ip = 0, ilen = 0;
    static BufferedInputStream bin = new BufferedInputStream(System.in, BUF);
    static long[] keys = new long[MAXN];
    static int[] tails = new int[MAXN];

    static int readByte() throws IOException {
        if (ip >= ilen) {
            ip = 0;
            ilen = bin.read(inbuf);
            if (ilen <= 0) {
                return -1;
            }
        }
        return inbuf[ip++];
    }

    static int nextInt() throws IOException {
        int c = readByte();
        while (c <= 32) {
            c = readByte();
        }
        int sig = 1;
        if (c == '-') {
            sig = -1;
            c = readByte();
        }
        int x = 0;
        while (c > 32) {
            x = x * 10 + (c - '0');
            c = readByte();
        }
        return x * sig;
    }

    static int lowerBound(int n, int x) {
        int l = 0, r = n;
        while (l < r) {
            int mid = (l + r) / 2;
            if (tails[mid] >= x) {
                r = mid;
            } else {
                l = mid + 1;
            }
        }
        return l;
    }

    static int maxBoats(int m) throws IOException {
        // 起点小的那条若终点不更小，就会追上或堵在终点
        for (int i = 0; i < m; i++) {
            keys[i] = ((long) nextInt()) << 32;
        }
        for (int i = 0; i < m; i++) {
            // 高 32 位是起点，低 32 位是终点取反，排序后即起点升序、终点降序
            keys[i] |= (0xffffffffL - nextInt());
        }
        Arrays.sort(keys, 0, m);
        int tn = 0;
        for (int i = 0; i < m; i++) {
            int d = (int) (0xffffffffL - (keys[i] & 0xffffffffL));
            int pos = lowerBound(tn, d);
            if (pos == tn) {
                tails[tn] = d;
                tn++;
            } else {
                tails[pos] = d;
            }
        }
        return tn;
    }

    public static void main(String[] args) throws IOException {
        int q = nextInt();
        for (int t = 0; t < q; t++) {
            int m = nextInt();
            System.out.println(maxBoats(m));
        }
    }
}
