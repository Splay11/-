import java.util.Scanner;

public class Main {
    static boolean canReduce(int[] vals) {
        int lo = vals[0], hi = vals[0];
        for (int x : vals) {
            if (x < lo) lo = x;
            if (x > hi) hi = x;
        }
        boolean[] seen = new boolean[hi - lo + 1];
        for (int x : vals) seen[x - lo] = true;
        for (boolean flag : seen) {
            if (!flag) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int k = sc.nextInt();
        for (int t = 0; t < k; t++) {
            int n = sc.nextInt();
            int[] vals = new int[n];
            for (int i = 0; i < n; i++) vals[i] = sc.nextInt();
            System.out.println(canReduce(vals) ? "YES" : "NO");
        }
        sc.close();
    }
}
