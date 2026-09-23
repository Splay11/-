import java.util.Scanner;

public class Main {
    // 去掉前导零；全零则保留单个 0
    static String normalize(String part) {
        int i = 0;
        while (i < part.length() - 1 && part.charAt(i) == '0') {
            i++;
        }
        return part.substring(i);
    }

    // 不能转 long：修订号可能超过 64 位；先比长度再比字典序
    static int comparePart(String a, String b) {
        if (a.length() != b.length()) {
            return a.length() > b.length() ? 1 : -1;
        }
        int cmp = a.compareTo(b);
        if (cmp != 0) {
            return cmp > 0 ? 1 : -1;
        }
        return 0;
    }

    static int compareVersion(String v1, String v2) {
        String[] p1 = v1.split("\\.", -1);
        String[] p2 = v2.split("\\.", -1);
        for (int i = 0; i < p1.length; i++) {
            p1[i] = normalize(p1[i]);
        }
        for (int i = 0; i < p2.length; i++) {
            p2[i] = normalize(p2[i]);
        }
        int n = Math.max(p1.length, p2.length);
        for (int i = 0; i < n; i++) {
            String a = i < p1.length ? p1[i] : "0";
            String b = i < p2.length ? p2[i] : "0";
            int c = comparePart(a, b);
            if (c != 0) {
                return c;
            }
        }
        return 0;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String v1 = sc.nextLine().trim();
        String v2 = sc.nextLine().trim();
        System.out.println(compareVersion(v1, v2));
        sc.close();
    }
}
