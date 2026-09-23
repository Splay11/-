import java.util.ArrayList;
import java.util.Scanner;

class Solution {
    public String solve(ArrayList<Integer> leftWeights, ArrayList<Integer> rightWeights) {
        // 请在这里实现
        return "";
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int m = sc.nextInt();

        ArrayList<Integer> leftWeights = new ArrayList<>();
        ArrayList<Integer> rightWeights = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            leftWeights.add(sc.nextInt());
        }
        for (int i = 0; i < m; i++) {
            rightWeights.add(sc.nextInt());
        }

        Solution solution = new Solution();
        System.out.println(solution.solve(leftWeights, rightWeights));

        sc.close();
    }
}
