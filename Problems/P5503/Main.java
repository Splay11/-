import java.util.Arrays;
import java.util.Scanner;

public class Main {
    // 展平后排序取第 K 大；总元素不超过 500*500
    static long kthLargest(long[] vals, int k) {
        Arrays.sort(vals);
        return vals[vals.length - k];
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int m = sc.nextInt();
        int k = sc.nextInt();
        long[] vals = new long[n * m];
        int idx = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                vals[idx++] = sc.nextLong();
            }
        }
        System.out.println(kthLargest(vals, k));
        sc.close();
    }
}
