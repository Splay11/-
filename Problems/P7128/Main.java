import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    static class Node {
        int val;
        Node next;
        Node(int v) {
            val = v;
        }
    }

    // 把数组建成单链表，返回头节点
    static Node buildList(int[] vals) {
        Node dummy = new Node(0);
        Node cur = dummy;
        for (int v : vals) {
            cur.next = new Node(v);
            cur = cur.next;
        }
        return dummy.next;
    }

    // 把长度为 n 的单链表向右旋转 k 位
    static Node rotateRight(Node head, int n, int k) {
        if (n == 0 || head == null) {
            return null;
        }
        k %= n;
        if (k == 0) {
            return head;
        }
        // 先走到尾并收成环，再数 n-k 步断开
        Node tail = head;
        while (tail.next != null) {
            tail = tail.next;
        }
        tail.next = head;
        int steps = n - k;
        Node newTail = head;
        for (int i = 0; i < steps - 1; i++) {
            newTail = newTail.next;
        }
        Node newHead = newTail.next;
        newTail.next = null;
        return newHead;
    }

    static List<Integer> toList(Node head) {
        List<Integer> out = new ArrayList<>();
        for (Node cur = head; cur != null; cur = cur.next) {
            out.add(cur.val);
        }
        return out;
    }

    static List<Integer> rotateVals(int[] vals, int k) {
        Node head = buildList(vals);
        head = rotateRight(head, vals.length, k);
        return toList(head);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        long k = Long.parseLong(st.nextToken());
        if (n == 0) {
            // 空链表输出空行
            System.out.println();
            return;
        }
        st = new StringTokenizer(br.readLine());
        int[] vals = new int[n];
        for (int i = 0; i < n; i++) {
            vals[i] = Integer.parseInt(st.nextToken());
        }
        int kk = (int) (k % n);
        List<Integer> ans = rotateVals(vals, kk);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(ans.get(i));
        }
        System.out.println(sb);
    }
}
