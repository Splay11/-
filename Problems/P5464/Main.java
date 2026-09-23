import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    static final long NEG = -(1L << 60);

    // 三段 DP：尚未加速 / 正在加速 / 加速已结束
    // d0 整段没加速；d1 当前项在窗口内；d2 窗口已结束
    static long maxGain(long[] v) {
        long d0 = v[0];
        long d1 = 2 * v[0];
        long d2 = NEG;
        long ans = d0 > d1 ? d0 : d1;
        for (int i = 1; i < v.length; i++) {
            long x = v[i];
            long t = 2 * x;
            // 不加速
            long nd0 = x > d0 + x ? x : d0 + x;
            // 正在加速：新开窗口 / 转入 / 继续
            long nd1 = t;
            if (d0 + t > nd1) {
                nd1 = d0 + t;
            }
            if (d1 + t > nd1) {
                nd1 = d1 + t;
            }
            // 加速已结束，只能加原值
            long nd2 = d1 + x;
            if (d2 + x > nd2) {
                nd2 = d2 + x;
            }
            d0 = nd0;
            d1 = nd1;
            d2 = nd2;
            if (d0 > ans) {
                ans = d0;
            }
            if (d1 > ans) {
                ans = d1;
            }
            if (d2 > ans) {
                ans = d2;
            }
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        // 单行最长约 2e5 个数，用 BufferedReader 读一整行
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int k = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int t = 0; t < k; t++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int m = Integer.parseInt(st.nextToken());
            long[] v = new long[m];
            for (int i = 0; i < m; i++) {
                v[i] = Long.parseLong(st.nextToken());
            }
            if (t > 0) {
                sb.append(' ');
            }
            sb.append(maxGain(v));
        }
        // 一行输出 k 个答案，空格隔开
        System.out.println(sb.toString());
    }
}
