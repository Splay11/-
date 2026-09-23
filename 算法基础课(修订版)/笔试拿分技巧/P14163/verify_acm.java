import java.util.ArrayList;
import java.util.Scanner;
import java.util.StringJoiner;

class Solution {
    public String solve(ArrayList<Integer> a) {
        StringJoiner joiner = new StringJoiner(" ");
        for (int value : a) {
            joiner.add(String.valueOf(value));
        }
        return joiner.toString();
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        ArrayList<Integer> a = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            a.add(sc.nextInt());
        }

        Solution solution = new Solution();
        System.out.print(solution.solve(a));
        sc.close();
    }
}
