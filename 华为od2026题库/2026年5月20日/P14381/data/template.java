import java.io.*;
import java.util.*;

public class Main {
    private static ArrayList<Integer> extractNumbers(String s) {
        ArrayList<Integer> nums = new ArrayList<Integer>();
        int n = s.length();
        for (int i = 0; i < n; i++) {
            if (Character.isDigit(s.charAt(i))) {
                int x = 0;
                while (i < n && Character.isDigit(s.charAt(i))) {
                    x = x * 10 + (s.charAt(i) - '0');
                    i++;
                }
                nums.add(x);
            }
        }
        return nums;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) {
            if (sb.length() > 0) sb.append(' ');
            sb.append(line);
        }

        ArrayList<Integer> nums = extractNumbers(sb.toString());
        int N = nums.get(0);
        int T = nums.get(1);

        int m = (nums.size() - 2) / 2;
        int[] accuracy = new int[m];
        int[] latency = new int[m];

        for (int i = 0; i < m; i++) accuracy[i] = nums.get(2 + i);
        for (int i = 0; i < m; i++) latency[i] = nums.get(2 + m + i);

        Solution solution = new Solution();
        System.out.print(solution.maxTotalAccuracy(N, T, accuracy, latency));
    }
}
