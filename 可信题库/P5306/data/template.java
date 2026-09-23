import java.io.*;
import java.util.regex.*;
public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        LeaseManager obj = null;
        String line;
        Pattern init = Pattern.compile("LeaseManager\\((-?\\d+)\\)");
        Pattern acquire = Pattern.compile("acquire\\((-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+)\\)");
        Pattern renew = Pattern.compile("renew\\((-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+)\\)");
        Pattern release = Pattern.compile("release\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern holder = Pattern.compile("holder\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern alive = Pattern.compile("aliveCount\\((-?\\d+)\\)");
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            Matcher m;
            if ((m = init.matcher(line)).matches()) {
                obj = new LeaseManager(Integer.parseInt(m.group(1)));
                System.out.println("null");
            } else if ((m = acquire.matcher(line)).matches()) {
                System.out.println(obj.acquire(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)), Integer.parseInt(m.group(3))));
            } else if ((m = renew.matcher(line)).matches()) {
                System.out.println(obj.renew(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)), Integer.parseInt(m.group(3))));
            } else if ((m = release.matcher(line)).matches()) {
                System.out.println(obj.release(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if ((m = holder.matcher(line)).matches()) {
                System.out.println(obj.holder(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if ((m = alive.matcher(line)).matches()) {
                System.out.println(obj.aliveCount(Integer.parseInt(m.group(1))));
            } else return;
        }
    }
}
