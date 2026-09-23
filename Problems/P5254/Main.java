import java.util.Scanner;

public class Main {
    static int countTriples(int n) {
        int ans = 0;
        // 枚举非降的 x、y，由异或还原 z
        for (int x = 1; x <= n; ++x) {
            for (int y = x; y <= n; ++y) {
                int z = x ^ y;
                if (y <= z && z <= n && x + y > z) {
                    ++ans;
                }
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        System.out.println(countTriples(n));
        sc.close();
    }
}
