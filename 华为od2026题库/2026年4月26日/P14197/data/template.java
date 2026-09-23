import java.io.*;
import java.util.*;

public class Main {
    private static int[] parseIntArray(String s) {
        s = s.trim();
        if (s.length() <= 2) return new int[0];
        s = s.substring(1, s.length() - 1).trim();
        if (s.length() == 0) return new int[0];

        String[] parts = s.split(",");
        int[] arr = new int[parts.length];
        for (int i = 0; i < parts.length; i++) {
            arr[i] = Integer.parseInt(parts[i].trim());
        }
        return arr;
    }

    private static void printIntArray(int[] arr) {
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < arr.length; i++) {
            if (i > 0) sb.append(",");
            sb.append(arr[i]);
        }
        sb.append("]");
        System.out.println(sb.toString());
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;

        int[] portRates = parseIntArray(line);
        Solution solution = new Solution();
        int[] ans = solution.StatPortRates(portRates);
        printIntArray(ans);
    }
}
