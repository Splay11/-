import java.util.ArrayList;
import java.util.Scanner;

class Solution {
    public int[] solve(int[] arr) {
        int maxValue = arr[0];
        for (int x : arr) {
            maxValue = Math.max(maxValue, x);
        }
        ArrayList<Integer> idx = new ArrayList<>();
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == maxValue) idx.add(i);
        }
        int[] result = new int[1 + idx.size()];
        result[0] = maxValue;
        for (int i = 0; i < idx.size(); i++) {
            result[i + 1] = idx.get(i);
        }
        return result;
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
