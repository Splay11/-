import java.io.*;
import java.util.regex.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line;
        ShardLeaseManager obj = null;
        Pattern ctorRe = Pattern.compile("ShardLeaseManager\\((\\d+),\\s*(\\d+)\\)");
        Pattern acqRe = Pattern.compile("acquire\\((-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+)\\)");
        Pattern renRe = Pattern.compile("renew\\((-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+)\\)");
        Pattern relRe = Pattern.compile("release\\((-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+)\\)");
        Pattern ownRe = Pattern.compile("owner\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern heldRe = Pattern.compile("heldCount\\((-?\\d+),\\s*(-?\\d+)\\)");
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            if (line.startsWith("ShardLeaseManager(")) {
                Matcher m = ctorRe.matcher(line);
                if (!m.matches()) throw new Exception("bad ctor");
                obj = new ShardLeaseManager(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)));
                System.out.println("null");
            } else if (line.startsWith("acquire(")) {
                Matcher m = acqRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.acquire(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)),
                        Integer.parseInt(m.group(3)), Integer.parseInt(m.group(4))));
            } else if (line.startsWith("renew(")) {
                Matcher m = renRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.renew(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)),
                        Integer.parseInt(m.group(3)), Integer.parseInt(m.group(4))));
            } else if (line.startsWith("release(")) {
                Matcher m = relRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.release(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)),
                        Integer.parseInt(m.group(3))));
            } else if (line.startsWith("owner(")) {
                Matcher m = ownRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.owner(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if (line.startsWith("heldCount(")) {
                Matcher m = heldRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.heldCount(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else {
                throw new Exception("bad op");
            }
        }
    }
}
