import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    // 每人 each 颗时，每堆能切出 candies[i] / each 份；份数够 k 个小孩即可
    static boolean canGive(int[] candies, long k, int each) {
        if (each == 0) {
            return true;
        }
        long got = 0;
        for (int i = 0; i < candies.length; i++) {
            got += candies[i] / each;
            if (got >= k) {
                return true;
            }
        }
        return false;
    }

    // 答案越大越难满足，在 [0, max(candies)] 上二分最大可行值
    static int maxCandies(int[] candies, long k) {
        int left = 0;
        int right = candies[0];
        for (int i = 1; i < candies.length; i++) {
            if (candies[i] > right) {
                right = candies[i];
            }
        }
        while (left < right) {
            int mid = left + (right - left + 1) / 2;
            if (canGive(candies, k, mid)) {
                left = mid;
            } else {
                right = mid - 1;
            }
        }
        return left;
    }

    public static void main(String[] args) throws IOException {
        // n 可达 1e5，k 可达 1e12，用 BufferedReader
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        long k = Long.parseLong(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] candies = new int[n];
        for (int i = 0; i < n; i++) {
            candies[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(maxCandies(candies, k));
    }
}
