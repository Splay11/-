import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {

    static class Zone implements Comparable<Zone> {
        int L, R;

        Zone(int L, int R) {
            this.L = L;
            this.R = R;
        }

        @Override
        public int compareTo(Zone other) {
            if (this.L != other.L) {
                return this.L - other.L;
            }
            return this.R - other.R;
        }
    }

    static int solveCase(int k, int s, Zone[] zones) {
        Arrays.sort(zones);

        int curL = zones[0].L;
        int curR = zones[0].R;

        for (int i = 1; i < k; i++) {
            int L = zones[i].L;
            int R = zones[i].R;

            if (L <= curR + 1) {
                if (R > curR) {
                    curR = R;
                }
            } else {
                if (curL <= s && s <= curR) {
                    return Math.min(s - curL + 1, curR - s + 1);
                }
                curL = L;
                curR = R;
            }
        }

        if (curL <= s && s <= curR) {
            return Math.min(s - curL + 1, curR - s + 1);
        }

        return 0;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        StringBuilder sb = new StringBuilder();

        int T = fs.nextInt();
        while (T-- > 0) {
            int k = fs.nextInt();
            int s = fs.nextInt();

            Zone[] zones = new Zone[k];
            for (int i = 0; i < k; i++) {
                zones[i] = new Zone(fs.nextInt(), fs.nextInt());
            }

            sb.append(solveCase(k, s, zones)).append('\n');
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
    }
}
