import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
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

    // 快指针先走 k 步，再和慢指针一起走，慢指针停在倒数第 k 个
    static int kthFromEnd(Node head, int k) {
        Node fast = head;
        for (int i = 0; i < k; i++) {
            fast = fast.next;
        }
        Node slow = head;
        while (fast != null) {
            fast = fast.next;
            slow = slow.next;
        }
        return slow.val;
    }

    static int solve(int[] vals, int k) {
        Node head = buildList(vals);
        return kthFromEnd(head, k);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] vals = new int[n];
        for (int i = 0; i < n; i++) {
            vals[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(solve(vals, k));
    }
}
