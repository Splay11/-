import java.io.*;
import java.util.*;

public class Main {
    private static int splitPos(String s) {
        int bracket = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '[') bracket++;
            else if (c == ']') bracket--;
            else if (c == ',' && bracket == 0) return i;
        }
        return -1;
    }

    private static int[] parseIntList(String s) {
        ArrayList<Integer> list = new ArrayList<>();
        int n = s.length(), i = 0;
        while (i < n) {
            while (i < n && !(s.charAt(i) == '-' || Character.isDigit(s.charAt(i)))) i++;
            if (i >= n) break;
            int sign = 1;
            if (s.charAt(i) == '-') {
                sign = -1;
                i++;
            }
            int x = 0;
            while (i < n && Character.isDigit(s.charAt(i))) {
                x = x * 10 + (s.charAt(i) - '0');
                i++;
            }
            list.add(sign * x);
        }
        int[] arr = new int[list.size()];
        for (int j = 0; j < list.size(); j++) arr[j] = list.get(j);
        return arr;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        int p = splitPos(line);
        String aStr = line.substring(0, p);
        String bStr = line.substring(p + 1);

        int[] cardA = parseIntList(aStr);
        int[] cardB = parseIntList(bStr);

        Solution solution = new Solution();
        System.out.print(solution.catFishCardGame(cardA, cardB));
    }
}
