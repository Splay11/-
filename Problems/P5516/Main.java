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
        int[] left = new int[n];
        int[] right = new int[n];
        for (int i = 0; i < n; i++) {
            left[i] = 1;
            right[i] = 1;
        }
        // 以 i 结尾的最长严格递增
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (a[j] < a[i] && left[j] + 1 > left[i]) {
                    left[i] = left[j] + 1;
                }
            }
        }
        // 以 i 开头的最长严格递减
        for (int i = n - 1; i >= 0; i--) {
            for (int j = i + 1; j < n; j++) {
                if (a[j] < a[i] && right[j] + 1 > right[i]) {
                    right[i] = right[j] + 1;
                }
            }
        }
        int ans = 0;
        for (int i = 0; i < n; i++) {
            if (left[i] >= 2 && right[i] >= 2) {
                ans = Math.max(ans, left[i] + right[i] - 1);
            }
        }
        System.out.println(ans);
    }
}
