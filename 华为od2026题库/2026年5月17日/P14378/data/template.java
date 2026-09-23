import java.io.*;
import java.util.*;

class Main {
    private static List<String> splitInput(String text) {
        List<String> parts = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        boolean inQuote = false;
        boolean escape = false;

        for (int i = 0; i < text.length(); i++) {
            char ch = text.charAt(i);
            if (escape) {
                current.append(ch);
                escape = false;
                continue;
            }
            if (ch == '\\') {
                current.append(ch);
                escape = true;
                continue;
            }
            if (ch == '"') {
                current.append(ch);
                inQuote = !inQuote;
                continue;
            }
            if (ch == ',' && !inQuote) {
                parts.add(current.toString().trim());
                current.setLength(0);
            } else {
                current.append(ch);
            }
        }
        parts.add(current.toString().trim());
        return parts;
    }

    private static String parseStringToken(String token) {
        token = token.trim();
        if (token.length() >= 2 && token.charAt(0) == '"' && token.charAt(token.length() - 1) == '"') {
            return token.substring(1, token.length() - 1);
        }
        return token;
    }

    public static void main(String[] args) throws Exception {
        StringBuilder input = new StringBuilder();
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line;
        while ((line = br.readLine()) != null) {
            input.append(line).append('\n');
        }

        List<String> parts = splitInput(input.toString());
        String preorderStr;
        String inorderStr;
        char beDeletedNode;

        if (parts.size() != 3) {
            preorderStr = "";
            inorderStr = "";
            beDeletedNode = '\0';
        } else {
            preorderStr = parseStringToken(parts.get(0));
            inorderStr = parseStringToken(parts.get(1));
            String deletedToken = parseStringToken(parts.get(2));
            beDeletedNode = deletedToken.length() == 1 ? deletedToken.charAt(0) : '\0';
        }

        String ans = new Solution().buildAfterDelete(preorderStr, inorderStr, beDeletedNode);
        if (ans == null) {
            ans = "";
        }
        System.out.println("\"" + ans + "\"");
    }
}
