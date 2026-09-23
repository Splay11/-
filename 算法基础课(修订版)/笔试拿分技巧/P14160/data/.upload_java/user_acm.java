import java.util.ArrayList;
import java.util.Scanner;

class Solution {
    public long solve(ArrayList<Long> a) {
        // 请在这里实现
        return 0;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        ArrayList<Long> a = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            a.add(sc.nextLong());
        }

        Solution solution = new Solution();
        System.out.println(solution.solve(a));
        sc.close();
    }
}
