import java.nio.charset.StandardCharsets;
import java.util.Scanner;

public class Main {
    // Bash 博弈：n 能被 k+1 整除则后手胜，否则先手胜
    static String whoWins(long n, long k) {
        // 每 k+1 颗构成一轮：先手若面对 k+1 的倍数，无论取 1~k 颗，
        // 后手都能取到刚好补成 k+1，把倍数局面丢回给先手
        if (n % (k + 1) == 0) {
            return "后手";
        }
        return "先手";
    }

    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        long n = sc.nextLong();
        long k = sc.nextLong();
        // 按 UTF-8 写出中文，避免评测机默认编码不一致
        System.out.write(whoWins(n, k).getBytes(StandardCharsets.UTF_8));
        System.out.write('\n');
        sc.close();
    }
}
