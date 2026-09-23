import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        StringBuilder builder = new StringBuilder();
        String line;

        while ((line = reader.readLine()) != null) {
            if (builder.length() > 0) {
                builder.append(' ');
            }
            builder.append(line);
        }

        String data = builder.toString().trim();
        data = data.replace('"', ' ').replace(',', ' ');

        Scanner scanner = new Scanner(data);
        String inputStr = "";
        int inputDivisor = 0;

        if (scanner.hasNext()) {
            inputStr = scanner.next();
        }
        if (scanner.hasNextInt()) {
            inputDivisor = scanner.nextInt();
        }

        Solution solution = new Solution();
        int result = solution.getMaxDivisibleNumber(inputStr, inputDivisor);
        System.out.println(result);

        scanner.close();
    }
}
