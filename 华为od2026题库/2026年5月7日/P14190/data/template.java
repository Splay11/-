import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        NumberReader reader = new NumberReader(System.in);
        ArrayList<Integer> values = reader.readAllNumbers();
        if (values.isEmpty()) {
            return;
        }

        int optimize = values.remove(values.size() - 1);
        int[] goodProceeTime = new int[values.size()];
        for (int i = 0; i < values.size(); i++) {
            goodProceeTime[i] = values.get(i);
        }

        Solution solution = new Solution();
        System.out.println(solution.minProcessTime(goodProceeTime, optimize));
    }

    static class NumberReader {
        private final InputStream in;
        byte[] buffer = new byte[1 << 12];
        private int ptr = 0, len = 0;

        NumberReader(InputStream in) {
            this.in = in;
        }

        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) {
                    return -1;
                }
            }
            return buffer[ptr++];
        }

        ArrayList<Integer> readAllNumbers() throws IOException {
            ArrayList<Integer> values = new ArrayList<>();
            int c = read();
            while (c != -1) {
                if (c >= '0' && c <= '9') {
                    int value = 0;
                    while (c >= '0' && c <= '9') {
                        value = value * 10 + (c - '0');
                        c = read();
                    }
                    values.add(value);
                } else {
                    c = read();
                }
            }
            return values;
        }
    }
}
