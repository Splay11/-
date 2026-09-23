import java.io.*;

/** 本地 ACM 自测用；OJ 核心代码模式以 data/template.java + data/user.java 为准。 */
public class Main {
    public static String packFields(int[] sectionWidth, int[] sectionValues) {
        long acc = 0;
        int total = 0;
        for (int i = 0; i < sectionWidth.length; i++) {
            int w = sectionWidth[i];
            acc = (acc << w) | (sectionValues[i] & 0xFFFFFFFFL);
            total += w;
        }
        int pad = (8 - total % 8) % 8;
        acc <<= pad;
        total += pad;
        int nbytes = total / 8;
        char[] hex = "0123456789ABCDEF".toCharArray();
        char[] ans = new char[nbytes * 2];
        for (int i = nbytes - 1; i >= 0; i--) {
            int b = (int) (acc & 0xFF);
            acc >>= 8;
            ans[i * 2] = hex[b >> 4];
            ans[i * 2 + 1] = hex[b & 0xF];
        }
        return new String(ans);
    }

    private static int[] parseIntArray(String line) {
        line = line.trim();
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
        String ans = packFields(parseIntArray(line1), parseIntArray(line2));
        System.out.println("\"" + ans + "\"");
    }
}
