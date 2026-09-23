import java.io.*;
import java.util.regex.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        JobQueueSys obj = null;
        Pattern init = Pattern.compile("JobQueueSys\\(\\)");
        Pattern submit = Pattern.compile("submit\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern cancel = Pattern.compile("cancel\\((-?\\d+)\\)");
        Pattern pop = Pattern.compile("popJob\\(\\)");
        Pattern peek = Pattern.compile("peekJob\\(\\)");
        String line;
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            Matcher m;
            if ((m = init.matcher(line)).matches()) {
                obj = new JobQueueSys();
                System.out.println("null");
            } else if ((m = submit.matcher(line)).matches()) {
                boolean ok = obj.submit(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)));
                System.out.println(ok ? "true" : "false");
            } else if ((m = cancel.matcher(line)).matches()) {
                boolean ok = obj.cancel(Integer.parseInt(m.group(1)));
                System.out.println(ok ? "true" : "false");
            } else if ((m = pop.matcher(line)).matches()) {
                System.out.println(obj.popJob());
            } else if ((m = peek.matcher(line)).matches()) {
                System.out.println(obj.peekJob());
            } else {
                throw new RuntimeException("bad op: " + line);
            }
        }
    }
}
