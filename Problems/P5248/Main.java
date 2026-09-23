import java.util.Scanner;

public class Main {
    static final int[] ODDS = {3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41};

    static int gcd(int a, int b) {
        while (b != 0) {
            int t = a % b;
            a = b;
            b = t;
        }
        return a;
    }

    static boolean impossible(int n) {
        return n <= 9 || n == 11 || n == 13 || n == 17;
    }

    static int[] solve(int n) {
        if (impossible(n)) {
            return null;
        }
        if (n % 2 == 0) {
            if (n % 6 != 2) {
                return new int[] {2, 3, n - 5};
            }
            return new int[] {3, 4, n - 7};
        }
        for (int i = 0; i < ODDS.length; i++) {
            int a = ODDS[i];
            for (int j = i; j < ODDS.length; j++) {
                int b = ODDS[j];
                if (gcd(a, b) != 1) {
                    continue;
                }
                int c = n - a - b;
                if (c >= 2 && gcd(a, c) == 1 && gcd(b, c) == 1) {
                    return new int[] {a, b, c};
                }
            }
        }
        return null;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int q = sc.nextInt();
        StringBuilder sb = new StringBuilder();
        for (int t = 0; t < q; t++) {
            int n = sc.nextInt();
            int[] ans = solve(n);
            if (ans == null) {
                sb.append(-1).append('\n');
            } else {
                sb.append(ans[0]).append(' ').append(ans[1]).append(' ').append(ans[2]).append('\n');
            }
        }
        System.out.print(sb);
        sc.close();
    }
}
