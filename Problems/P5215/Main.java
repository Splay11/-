import java.io.*;
import java.util.*;

public class Main {
    // 任意划分的贡献之和不超过 (全局 max - 全局 min) * n，整段取满即可。
    static long maxFluctuation(int n, long[] v) {
        long mn = v[0], mx = v[0];
        for (int i = 1; i < n; i++) {
            if (v[i] < mn) mn = v[i];
            if (v[i] > mx) mx = v[i];
        }
        return (mx - mn) * n;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        long[] v = new long[n];
        for (int i = 0; i < n; i++) {
            v[i] = Long.parseLong(st.nextToken());
        }
        System.out.println(maxFluctuation(n, v));
    }
}
