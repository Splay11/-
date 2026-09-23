import java.io.*;
import java.util.regex.*;

public class Main {
    private static final Pattern INIT = Pattern.compile("MemMgmtSys\\((\\d+)\\)");
    private static final Pattern ALLOC = Pattern.compile("processMemAlloc\\((-?\\d+),\\s*(-?\\d+)\\)");
    private static final Pattern FREE = Pattern.compile("processMemFree\\((-?\\d+)\\)");
    private static final Pattern QUERY = Pattern.compile("processMemQuery\\((-?\\d+)\\)");

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        String line;
        MemMgmtSys obj = null;
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            Matcher m;
            if ((m = INIT.matcher(line)).matches()) {
                obj = new MemMgmtSys(Integer.parseInt(m.group(1)));
                sb.append("null\n");
            } else if ((m = ALLOC.matcher(line)).matches()) {
                sb.append(obj.processMemAlloc(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)))).append('\n');
            } else if ((m = FREE.matcher(line)).matches()) {
                obj.processMemFree(Integer.parseInt(m.group(1)));
                sb.append("null\n");
            } else if ((m = QUERY.matcher(line)).matches()) {
                sb.append(obj.processMemQuery(Integer.parseInt(m.group(1)))).append('\n');
            } else {
                throw new RuntimeException("bad op: " + line);
            }
        }
        System.out.print(sb.toString());
    }
}
