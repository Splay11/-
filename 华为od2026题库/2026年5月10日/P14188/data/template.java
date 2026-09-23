import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        String line;

        while ((line = br.readLine()) != null) {
            sb.append(line);
        }

        String text = sb.toString().trim();
        List<Integer> nums = new ArrayList<>();

        text = text.replace('[', ' ')
                   .replace(']', ' ')
                   .replace(',', ' ');

        Scanner scanner = new Scanner(text);
        while (scanner.hasNextInt()) {
            nums.add(scanner.nextInt());
        }
        scanner.close();

        int[] arr = new int[nums.size()];
        for (int i = 0; i < nums.size(); i++) {
            arr[i] = nums.get(i);
        }

        Solution solution = new Solution();
        int[] ans = solution.longestBeautifulLanterns(arr);

        System.out.println("[" + ans[0] + "," + ans[1] + "]");
    }
}
