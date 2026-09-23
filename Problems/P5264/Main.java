import java.io.*;
import java.util.*;

public class Main {
    static class FastScanner {
        private final InputStream in;
        private final byte[] buf = new byte[1 << 16];
        private int ptr, len;

        FastScanner(InputStream in) {
            this.in = in;
        }

        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buf);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buf[ptr++];
        }

        String next() throws IOException {
            StringBuilder sb = new StringBuilder();
            int c;
            while ((c = read()) <= ' ') {
                if (c == -1) return null;
            }
            do {
                sb.append((char) c);
                c = read();
            } while (c > ' ');
            return sb.toString();
        }

        int nextInt() throws IOException {
            return Integer.parseInt(next());
        }

        double nextDouble() throws IOException {
            return Double.parseDouble(next());
        }
    }

    static class State {
        double mx, wd, sv;

        State(double mx, double wd, double sv) {
            this.mx = mx;
            this.wd = wd;
            this.sv = sv;
        }
    }

    static State merge(State a, State b) {
        double mx = Math.max(a.mx, b.mx);
        double ea = Math.exp(a.mx - mx);
        double eb = Math.exp(b.mx - mx);
        return new State(mx, a.wd * ea + b.wd * eb, a.sv * ea + b.sv * eb);
    }

    static class SegTree {
        int size;
        State[] tree;

        SegTree(State[] blocks) {
            int n = blocks.length;
            size = 1;
            while (size < n) size <<= 1;
            tree = new State[2 * size];
            for (int i = 0; i < 2 * size; i++) tree[i] = new State(0, 0, 0);
            for (int i = 0; i < n; i++) tree[size + i] = blocks[i];
            for (int i = size - 1; i >= 1; i--)
                tree[i] = merge(tree[i * 2], tree[i * 2 + 1]);
        }

        void update(int pos, State val) {
            int i = size + pos;
            tree[i] = val;
            for (i /= 2; i >= 1; i /= 2)
                tree[i] = merge(tree[i * 2], tree[i * 2 + 1]);
        }

        State query(int l, int r) {
            l += size;
            r += size;
            boolean hasL = false, hasR = false;
            State left = null, right = null;
            while (l <= r) {
                if ((l & 1) == 1) {
                    left = hasL ? merge(left, tree[l]) : tree[l];
                    hasL = true;
                    l++;
                }
                if ((r & 1) == 0) {
                    right = hasR ? merge(tree[r], right) : tree[r];
                    hasR = true;
                    r--;
                }
                l /= 2;
                r /= 2;
            }
            if (!hasL) return right;
            if (!hasR) return left;
            return merge(left, right);
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        int B = fs.nextInt();
        int Q = fs.nextInt();
        State[] blocks = new State[B];
        for (int i = 0; i < B; i++)
            blocks[i] = new State(fs.nextDouble(), fs.nextDouble(), fs.nextDouble());
        SegTree seg = new SegTree(blocks);
        StringBuilder sb = new StringBuilder(Q * 12);
        for (int t = 0; t < Q; t++) {
            int op = fs.nextInt();
            if (op == 1) {
                int i = fs.nextInt() - 1;
                seg.update(i, new State(fs.nextDouble(), fs.nextDouble(), fs.nextDouble()));
            } else {
                int l = fs.nextInt() - 1;
                int r = fs.nextInt() - 1;
                State res = seg.query(l, r);
                sb.append(String.format(Locale.US, "%.6f%n", res.sv / res.wd));
            }
        }
        System.out.print(sb);
    }
}
