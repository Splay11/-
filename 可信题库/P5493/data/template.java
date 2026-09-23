import java.io.*;
import java.util.regex.*;

public class Main {
    private static String fmtFiles(int[][] a) {
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append('[').append(a[i][0]).append(", ").append(a[i][1]).append(", ").append(a[i][2]).append(']');
        }
        sb.append(']');
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line;
        FileLogger obj = null;
        Pattern ctorRe = Pattern.compile("FileLogger\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern appRe = Pattern.compile("putLog\\((-?\\d+),\\s*(-?\\d+)\\)");
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            if (line.startsWith("FileLogger(")) {
                Matcher m = ctorRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                obj = new FileLogger(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)));
                System.out.println("null");
            } else if (line.startsWith("putLog(")) {
                Matcher m = appRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.putLog(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if (line.equals("listFiles()")) {
                System.out.println(fmtFiles(obj.listFiles()));
            } else if (line.equals("totalSize()")) {
                System.out.println(obj.totalSize());
            } else {
                throw new Exception("bad op");
            }
        }
    }
}
