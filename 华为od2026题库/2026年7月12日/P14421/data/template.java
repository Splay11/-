import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String s = br.readLine();
        if (s == null) s = "";
        Solution solution = new Solution();
        System.out.println(solution.compress(s));
    }
}
