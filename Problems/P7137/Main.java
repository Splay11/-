import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    // 判断每段长度为 length 时，能不能切出至少 k 段
    // 段数可能到 1e14，用 long，累加到 >= k 就提前停
    static boolean canCut(int[] a, long k, int length) {
        long got = 0;
        for (int x : a) {
            got += x / length;
            if (got >= k) {
                return true;
            }
        }
        return false;
    }

    // 二分答案：长度越大越难切够 k 段。题目保证长度为 1 一定可行
    static int solve(int[] a, long k) {
        int left = 1;
        int right = a[0];
        for (int i = 1; i < a.length; i++) {
            if (a[i] > right) {
                right = a[i];
            }
        }
        int ans = 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (canCut(a, k, mid)) {
                // mid 可行，试更长的
                ans = mid;
                left = mid + 1;
            } else {
                // mid 太长，切不够，往短了找
                right = mid - 1;
            }
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        long k = Long.parseLong(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(solve(a, k));
    }
}
