import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String[] sp = br.readLine().trim().split("\\s+");
        long[] a = new long[n];
        for (int i = 0; i < n; i++) a[i] = Long.parseLong(sp[i]);

        // 前缀和与平方和
        double[] ps = new double[n + 1];
        double[] qs = new double[n + 1];
        for (int i = 0; i < n; i++) {
            ps[i + 1] = ps[i] + a[i];
            qs[i + 1] = qs[i] + (double) a[i] * a[i];
        }

        double best = -1.0;
        for (int k = 1; k < n; k++) {
            double n1 = k, n2 = n - k;
            // 方差 = E[x^2] - (E[x])^2
            double v1 = qs[k] / n1 - (ps[k] / n1) * (ps[k] / n1);
            double v2 = (qs[n] - qs[k]) / n2
                    - ((ps[n] - ps[k]) / n2) * ((ps[n] - ps[k]) / n2);
            if (v1 + v2 > best) best = v1 + v2;
        }
        System.out.printf(Locale.US, "%.6f%n", best);
    }
}
