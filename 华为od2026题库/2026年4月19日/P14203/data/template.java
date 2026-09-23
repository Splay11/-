import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class Main {
    private static char[][] parseRoomArrangement(String text) {
        List<char[]> rows = new ArrayList<>();
        List<Character> current = new ArrayList<>();
        for (int i = 0; i < text.length(); i++) {
            char ch = text.charAt(i);
            if (ch == '.' || ch == '#') {
                current.add(ch);
            } else if (ch == ']' && !current.isEmpty()) {
                char[] row = new char[current.size()];
                for (int j = 0; j < current.size(); j++) {
                    row[j] = current.get(j);
                }
                rows.add(row);
                current.clear();
            }
        }
        char[][] roomArrangement = new char[rows.size()][];
        for (int i = 0; i < rows.size(); i++) {
            roomArrangement[i] = rows.get(i);
        }
        return roomArrangement;
    }

    private static String readAll() throws Exception {
        InputStream in = System.in;
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] buffer = new byte[4096];
        int len;
        while ((len = in.read(buffer)) != -1) {
            out.write(buffer, 0, len);
        }
        return out.toString(StandardCharsets.UTF_8);
    }

    public static void main(String[] args) throws Exception {
        String text = readAll();
        char[][] roomArrangement = parseRoomArrangement(text);
        Solution solution = new Solution();
        int answer = solution.networkPlanning(roomArrangement);
        System.out.print(answer);
    }
}
