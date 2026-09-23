import java.util.*;

public class Main {
    static long solve(long[] a) {
        int n = a.length;
        long s = 0;
        for (long x : a) s += x;
        if (n % 2 == 0 && s % 2 == 1) return -1;
        long diff = 0;
        for (int i = 0; i < n / 2; i++)
            diff += Math.abs(a[i] - a[n - 1 - i]);
        return (diff + 1) / 2;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        while (T-- > 0) {
            int n = sc.nextInt();
            long[] a = new long[n];
            for (int i = 0; i < n; i++) a[i] = sc.nextLong();
            System.out.println(solve(a));
        }
        sc.close();
    }
}
