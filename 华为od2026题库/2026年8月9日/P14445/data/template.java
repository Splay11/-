import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        int firstComma = line.indexOf(',');
        int priceRecords = Integer.parseInt(line.substring(0, firstComma));

        String rest = line.substring(firstComma + 1);
        int secondComma = rest.indexOf(',');
        int hours = Integer.parseInt(rest.substring(0, secondComma));

        // 解析数组 [a,b,c,...]
        String arrStr = rest.substring(secondComma + 1);
        arrStr = arrStr.substring(1, arrStr.length() - 1);
        String[] parts = arrStr.split(",");
        int[] priceArray = new int[parts.length];
        for (int i = 0; i < parts.length; i++) {
            priceArray[i] = Integer.parseInt(parts[i].trim());
        }

        Solution solution = new Solution();
        System.out.println(solution.findBestChargingTime(priceRecords, hours, priceArray));
    }
}
