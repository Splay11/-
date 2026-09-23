import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Solution {
    public int[] solve(int[] arr, int l, int r) {
        l--;
        r--;
        int maxValue = arr[l];
        List<Integer> maxIndices = new ArrayList<>();
        maxIndices.add(l + 1);
        for (int i = l + 1; i <= r; ++i) {
            if (arr[i] > maxValue) {
                maxValue = arr[i];
                maxIndices.clear();
                maxIndices.add(i + 1);
            } else if (arr[i] == maxValue) {
                maxIndices.add(i + 1);
            }
        }
        int[] result = new int[1 + maxIndices.size()];
        result[0] = maxValue;
        for (int i = 0; i < maxIndices.size(); ++i) {
            result[i + 1] = maxIndices.get(i);
        }
        return result;
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
