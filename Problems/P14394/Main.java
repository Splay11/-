import java.util.ArrayDeque;
import java.util.HashSet;

public class Solution {
    public int[] processPacketCommands(String[] commands) {
        ArrayDeque<Integer> buffer = new ArrayDeque<>();  // 缓冲区
        ArrayDeque<Integer> sendQ = new ArrayDeque<>();   // 发送区
        HashSet<Integer> inBuffer = new HashSet<>();      // 缓冲区中的编号集合
        int[] ans = new int[commands.length];

        for (int i = 0; i < commands.length; i++) {
            String cmd = commands[i];
            if (cmd.startsWith("RECEIVE")) {
                int x = Integer.parseInt(cmd.substring("RECEIVE".length()).trim());
                // 仅检查缓冲区是否已有同编号
                if (inBuffer.contains(x)) {
                    ans[i] = -1;
                } else {
                    buffer.addLast(x);
                    inBuffer.add(x);
                    ans[i] = x;
                }
            } else if (cmd.equals("SEND")) {
                if (!sendQ.isEmpty()) {
                    // 发送区非空，弹出最早的数据包
                    ans[i] = sendQ.removeFirst();
                } else if (!buffer.isEmpty()) {
                    flush(buffer, sendQ, inBuffer);
                    ans[i] = sendQ.removeFirst();
                } else {
                    ans[i] = 0;  // 两区皆空
                }
            } else if (cmd.equals("QUERY")) {
                if (!sendQ.isEmpty()) {
                    ans[i] = sendQ.peekFirst();  // 只查队首，不弹出
                } else if (!buffer.isEmpty()) {
                    flush(buffer, sendQ, inBuffer);
                    ans[i] = sendQ.peekFirst();
                } else {
                    ans[i] = 0;
                }
            }
        }
        return ans;
    }

    private void flush(ArrayDeque<Integer> buffer, ArrayDeque<Integer> sendQ,
                       HashSet<Integer> inBuffer) {
        // 将缓冲区全部按 FIFO 移入发送区
        while (!buffer.isEmpty()) {
            int x = buffer.removeFirst();
            inBuffer.remove(x);
            sendQ.addLast(x);
        }
    }
}
