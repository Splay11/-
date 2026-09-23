import java.util.*;

public class Main {
    static int[] solve(int[] p, long k) {
        int n = p.length;
        long limit = 1L * n * (n - 1) / 2;
        if (k >= limit) {
            int[] a = p.clone();
            Arrays.sort(a);
            return a;
        }
        for (long t = 0; t < k; t++) {
            boolean swapped = false;
            for (int i = 0; i + 1 < n; i++) {
                if (p[i] > p[i + 1]) {
                    int tmp = p[i];
                    p[i] = p[i + 1];
                    p[i + 1] = tmp;
                    swapped = true;
                    break;
                }
            }
            if (!swapped) break;
        }
        return p;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        while (T-- > 0) {
            int n = sc.nextInt();
            long k = sc.nextLong();
            int[] p = new int[n];
            for (int i = 0; i < n; i++) p[i] = sc.nextInt();
            int[] ans = solve(p, k);
            for (int i = 0; i < n; i++) {
                if (i > 0) System.out.print(' ');
                System.out.print(ans[i]);
            }
            System.out.println();
        }
        sc.close();
    }
}
