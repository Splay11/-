import java.util.Scanner;

public class Main {
    static boolean canSplit(int[] layers, int m, int limit) {
        int cnt = 1;
        long s = 0;
        for (int x : layers) {
            if (s + x > limit) {
                cnt++;
                s = 0;
            }
            s += x;
        }
        return cnt <= m;
    }

    static int minBottleneck(int[] layers, int m) {
        int lo = 0, hi = 0;
        for (int x : layers) {
            lo = Math.max(lo, x);
            hi += x;
        }
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (canSplit(layers, m, mid)) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] layers = new int[n];
        for (int i = 0; i < n; i++) {
            layers[i] = sc.nextInt();
        }
        int m = sc.nextInt();
        System.out.println(minBottleneck(layers, m));
        sc.close();
    }
}
