import java.util.Scanner;

class Solution {
    public int solve(int n) {
        int count = 0;
        for (int i = 1; i <= n; i++) {
            int sumOfDigits = 0;
            int num = i;
            while (num > 0) {
                sumOfDigits += num % 10;
                num /= 10;
            }
            if (sumOfDigits % 10 == i % 10) {
                count++;
            }
        }
        return count;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();

        Solution solution = new Solution();
        System.out.println(solution.solve(n));

        scanner.close();
    }
}
