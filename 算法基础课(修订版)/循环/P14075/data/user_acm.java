import java.util.ArrayList;
import java.util.Scanner;

class Solution {
    public int[] solve(int[] arr) {
        // 请在这里实现
        // 返回 int[]{maxValue, index1, index2, ...}
        return new int[] {0};
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = scanner.nextInt();
        }

        Solution solution = new Solution();
        int[] result = solution.solve(arr);

        System.out.println(result[0]);
        for (int i = 1; i < result.length; i++) {
            System.out.print(result[i] + (i + 1 == result.length ? "" : " "));
        }
        System.out.println();

        scanner.close();
    }
}
