import java.io.*;
import java.util.regex.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line;
        CertAuthority obj = null;
        Pattern issueRe = Pattern.compile("issue\\((-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+)\\)");
        Pattern revRe = Pattern.compile("revoke\\((-?\\d+)\\)");
        Pattern validRe = Pattern.compile("isValid\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern ttlRe = Pattern.compile("ttl\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern issRe = Pattern.compile("issuerOf\\((-?\\d+)\\)");
        Pattern rootRe = Pattern.compile("rootOf\\((-?\\d+)\\)");
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            if (line.equals("CertAuthority()")) {
                obj = new CertAuthority();
                System.out.println("null");
            } else if (line.startsWith("issue(")) {
                Matcher m = issueRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.issue(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)), Integer.parseInt(m.group(3))));
            } else if (line.startsWith("revoke(")) {
                Matcher m = revRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.revoke(Integer.parseInt(m.group(1))));
            } else if (line.startsWith("isValid(")) {
                Matcher m = validRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.isValid(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if (line.startsWith("ttl(")) {
                Matcher m = ttlRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.ttl(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if (line.startsWith("issuerOf(")) {
                Matcher m = issRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.issuerOf(Integer.parseInt(m.group(1))));
            } else if (line.startsWith("rootOf(")) {
                Matcher m = rootRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.rootOf(Integer.parseInt(m.group(1))));
            } else {
                throw new Exception("bad op");
            }
        }
    }
}
