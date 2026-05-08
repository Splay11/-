import java.math.BigInteger;
import java.util.Scanner;

public class Main {
    static int solve(BigInteger n) {
        // bitLength 是二进制位数，减一后就是最高二进制位下标。
        return n.bitLength() - 1;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        BigInteger n = scanner.nextBigInteger();
        System.out.println(solve(n));
        scanner.close();
    }
}
