import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class Main {
    private static int[][] parseInput(String data) {
        // 输入格式：
        // [1, 1, 1, ...], [1, 2, 3, ...]
        // 这里把中括号、逗号等非数字字符统一替换为空格，再用输入流读取整数
        String cleaned = data.replaceAll("[^0-9]+", " ").trim();

        ArrayList<Integer> values = new ArrayList<>();
        if (!cleaned.isEmpty()) {
            Scanner scanner = new Scanner(cleaned);
            while (scanner.hasNextInt()) {
                values.add(scanner.nextInt());
            }
            scanner.close();
        }

        int[] colors = new int[14];
        int[] numbers = new int[14];

        for (int i = 0; i < 14; i++) {
            colors[i] = values.get(i);
        }

        for (int i = 0; i < 14; i++) {
            numbers[i] = values.get(i + 14);
        }

        return new int[][]{colors, numbers};
    }

    public static void main(String[] args) throws Exception {
        String data = new String(System.in.readAllBytes(), StandardCharsets.UTF_8);

        int[][] input = parseInput(data);

        Solution solution = new Solution();
        long ans = solution.countWinningHands(input[0], input[1]);

        System.out.println(ans);
    }
}
