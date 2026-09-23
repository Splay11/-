import java.io.*;
import java.util.regex.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        TTLCache obj = null;
        Pattern init = Pattern.compile("TTLCache\\((-?\\d+)\\)");
        Pattern put = Pattern.compile("put\\((-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+)\\)");
        Pattern get = Pattern.compile("get\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern purge = Pattern.compile("purge\\((-?\\d+)\\)");
        Pattern size = Pattern.compile("size\\(\\)");
        String line;
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            Matcher m;
            if ((m = init.matcher(line)).matches()) {
                obj = new TTLCache(Integer.parseInt(m.group(1)));
                System.out.println("null");
            } else if ((m = put.matcher(line)).matches()) {
                obj.put(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)), Integer.parseInt(m.group(3)));
                System.out.println("null");
            } else if ((m = get.matcher(line)).matches()) {
                System.out.println(obj.get(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if ((m = purge.matcher(line)).matches()) {
                System.out.println(obj.purge(Integer.parseInt(m.group(1))));
            } else if ((m = size.matcher(line)).matches()) {
                System.out.println(obj.size());
            } else {
                throw new RuntimeException("bad op: " + line);
            }
        }
    }
}
