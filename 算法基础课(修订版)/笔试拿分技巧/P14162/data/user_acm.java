import java.util.ArrayList;
import java.util.Scanner;

class Solution {
    public int solve(int n, int k, ArrayList<int[]> intervals) {
        // 请在这里实现
        return 0;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int k = sc.nextInt();
        ArrayList<int[]> intervals = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            intervals.add(new int[] {sc.nextInt(), sc.nextInt()});
        }

        Solution solution = new Solution();
        System.out.println(solution.solve(n, k, intervals));
        sc.close();
    }
}
