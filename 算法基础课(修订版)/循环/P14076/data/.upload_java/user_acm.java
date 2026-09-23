import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Solution {
    public int[] solve(int[] arr, int l, int r) {
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
        for (int i = 0; i < n; ++i) {
            arr[i] = scanner.nextInt();
        }

        int q = scanner.nextInt();
        Solution solution = new Solution();
        while (q-- > 0) {
            int l = scanner.nextInt();
            int r = scanner.nextInt();
            int[] result = solution.solve(arr, l, r);

            System.out.println(result[0]);
            for (int i = 1; i < result.length; ++i) {
                System.out.print(result[i]);
                if (i + 1 < result.length) {
                    System.out.print(" ");
                }
            }
            System.out.println();
        }

        scanner.close();
    }
}
