import java.util.ArrayList;
import java.util.Scanner;

class Solution {
    public int solve(ArrayList<Integer> times, ArrayList<int[]> mutexPairs) {
        // 请在这里实现
        return 0;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int jobNum = sc.nextInt();
        ArrayList<Integer> times = new ArrayList<>();
        for (int i = 0; i < jobNum; i++) {
            times.add(sc.nextInt());
        }

        int mutexNum = sc.nextInt();
        ArrayList<int[]> mutexPairs = new ArrayList<>();
        for (int i = 0; i < mutexNum; i++) {
            mutexPairs.add(new int[] {sc.nextInt(), sc.nextInt()});
        }

        Solution solution = new Solution();
        System.out.println(solution.solve(times, mutexPairs));
        sc.close();
    }
}
