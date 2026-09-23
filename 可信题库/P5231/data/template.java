import java.io.*;
import java.util.*;

public class Main {
    private static String trim(String s) {
        return s == null ? "" : s.trim();
    }

    private static int[] parseIntArray(String line) {
        line = trim(line);
        if (line.length() < 2 || line.charAt(0) != '[' || line.charAt(line.length() - 1) != ']')
            throw new RuntimeException("bad array");
        line = line.substring(1, line.length() - 1).trim();
        if (line.isEmpty()) return new int[0];
        String[] parts = line.split(",");
        int[] a = new int[parts.length];
        for (int i = 0; i < parts.length; i++) a[i] = Integer.parseInt(parts[i].trim());
        return a;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line1 = br.readLine();
        String line2 = br.readLine();
        if (line1 == null || line2 == null) return;
        int[] sectionWidth = parseIntArray(line1);
        int[] sectionValues = parseIntArray(line2);
        String ans = new Solution().packFields(sectionWidth, sectionValues);
        System.out.println("\"" + ans + "\"");
    }
}
