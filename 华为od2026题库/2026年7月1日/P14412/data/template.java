import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        // 解析数组 "[a1,a2,...,an]"
        line = line.substring(1, line.length() - 1);
        String[] parts = line.split(",");
        List<Integer> items = new ArrayList<>();
        for (String part : parts) {
            items.add(Integer.parseInt(part.trim()));
        }

        Solution solution = new Solution();
        List<Integer> result = solution.warehouseInventory(items);
        System.out.println(result.toString().replace(" ", ""));
    }
}
