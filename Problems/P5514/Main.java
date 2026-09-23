import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            a[i] = Long.parseLong(st.nextToken());
        }
        final long INF = Long.MAX_VALUE / 4;
        // f：选中当前位置；g：不选当前位置且已非空
        long f = a[0], g = INF;
        for (int i = 1; i < n; i++) {
            long ng = Math.min(f, g);
            long nf = a[i] + (g >= INF / 2 ? 0 : Math.min(0L, g));
            f = nf;
            g = ng;
        }
        System.out.println(Math.min(f, g));
    }
}
