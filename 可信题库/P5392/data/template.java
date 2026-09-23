import java.io.*;
import java.util.regex.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        FileLockBoard obj = null;
        Pattern init = Pattern.compile("FileLockBoard\\(\\)");
        Pattern lock = Pattern.compile("lock\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern unlock = Pattern.compile("unlock\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern holder = Pattern.compile("holder\\((-?\\d+)\\)");
        Pattern cnt = Pattern.compile("lockedCount\\(\\)");
        String line;
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            Matcher m;
            if ((m = init.matcher(line)).matches()) {
                obj = new FileLockBoard();
                System.out.println("null");
            } else if ((m = lock.matcher(line)).matches()) {
                System.out.println(obj.lock(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if ((m = unlock.matcher(line)).matches()) {
                System.out.println(obj.unlock(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if ((m = holder.matcher(line)).matches()) {
                System.out.println(obj.holder(Integer.parseInt(m.group(1))));
            } else if ((m = cnt.matcher(line)).matches()) {
                System.out.println(obj.lockedCount());
            } else {
                throw new RuntimeException("bad op: " + line);
            }
        }
    }
}
