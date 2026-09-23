// 注意：类名必须为 Main，ACM 风格从标准输入读取
import java.io.*;
import java.util.*;

public class Main {
    // 计算 x 中质因子 p 的个数（只会对 2 和 5 调用）
    static int countFactor(long x, int p) {
        int c = 0;
        while (x % p == 0) {
            x /= p;
            c++;
        }
        return c;
    }

    static long solve(int[] arr, long k) {
        int n = arr.length;
        int[] c2 = new int[n];
        int[] c5 = new int[n];
        for (int i = 0; i < n; i++) {
            c2[i] = countFactor(arr[i], 2);
            c5[i] = countFactor(arr[i], 5);
        }
        long ans = 0L;
        int l = 0, r = 0;
        long cur2 = 0, cur5 = 0;
        // 双指针窗口 [l, r)
        while (l < n) {
            while (r < n && (cur2 < k || cur5 < k)) {
                cur2 += c2[r];
                cur5 += c5[r];
                r++;
            }
            if (cur2 >= k && cur5 >= k) {
                ans += (n - r + 1);
            }
            cur2 -= c2[l];
            cur5 -= c5[l];
            l++;
        }
        return ans;
    }

    public static void main(String[] args) throws Exception {
        // 根据数据规模使用 BufferedReader + StringTokenizer
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        long k = Long.parseLong(st.nextToken());

        st = new StringTokenizer(br.readLine());
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = Integer.parseInt(st.nextToken());

        System.out.println(solve(a, k));
    }
}
