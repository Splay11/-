import java.io.*;
import java.util.regex.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        MicQueue obj = null;
        Pattern init = Pattern.compile("MicQueue\\(\\)");
        Pattern enroll = Pattern.compile("enroll\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern nextPlay = Pattern.compile("nextPlay\\(\\)");
        Pattern boost = Pattern.compile("boost\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern cancel = Pattern.compile("cancel\\((-?\\d+)\\)");
        Pattern waiting = Pattern.compile("waiting\\(\\)");
        String line;
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            Matcher m;
            if ((m = init.matcher(line)).matches()) {
                obj = new MicQueue();
                System.out.println("null");
            } else if ((m = enroll.matcher(line)).matches()) {
                System.out.println(obj.enroll(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if ((m = nextPlay.matcher(line)).matches()) {
                System.out.println(obj.nextPlay());
            } else if ((m = boost.matcher(line)).matches()) {
                System.out.println(obj.boost(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if ((m = cancel.matcher(line)).matches()) {
                System.out.println(obj.cancel(Integer.parseInt(m.group(1))));
            } else if ((m = waiting.matcher(line)).matches()) {
                System.out.println(obj.waiting());
            } else {
                throw new RuntimeException("bad op: " + line);
            }
        }
    }
}
