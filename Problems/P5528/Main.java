import java.io.*;
import java.util.*;

public class Main {
    static class Node {
        int key, value;
        long expire;
        Node prev, next;
        Node(int k, int v, long e) {
            key = k;
            value = v;
            expire = e;
        }
    }

    static class TTLLRU {
        int cap;
        HashMap<Integer, Node> mp = new HashMap<>();
        Node head, tail; // head 后最久未用，tail 前最近

        TTLLRU(int c) {
            cap = c;
            head = new Node(0, 0, 0);
            tail = new Node(0, 0, 0);
            head.next = tail;
            tail.prev = head;
        }

        void remove(Node x) {
            x.prev.next = x.next;
            x.next.prev = x.prev;
        }

        void addBack(Node x) {
            x.prev = tail.prev;
            x.next = tail;
            tail.prev.next = x;
            tail.prev = x;
        }

        boolean expired(Node x, long ts) {
            return x.expire <= ts;
        }

        void evict(long ts) {
            // 优先淘汰已过期
            for (Node p = head.next; p != tail; p = p.next) {
                if (expired(p, ts)) {
                    mp.remove(p.key);
                    remove(p);
                    return;
                }
            }
            // 否则淘汰 LRU
            Node p = head.next;
            mp.remove(p.key);
            remove(p);
        }

        void put(int key, int value, int ttl, long ts) {
            long exp = ts + ttl;
            if (mp.containsKey(key)) {
                Node x = mp.get(key);
                x.value = value;
                x.expire = exp;
                remove(x);
                addBack(x);
                return;
            }
            if (mp.size() >= cap) evict(ts);
            Node x = new Node(key, value, exp);
            mp.put(key, x);
            addBack(x);
        }

        int get(int key, long ts) {
            if (!mp.containsKey(key)) return -1;
            Node x = mp.get(key);
            if (expired(x, ts)) {
                mp.remove(key);
                remove(x);
                return -1;
            }
            remove(x);
            addBack(x);
            return x.value;
        }
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int capacity = Integer.parseInt(st.nextToken());
        int q = Integer.parseInt(st.nextToken());
        TTLLRU cache = new TTLLRU(capacity);
        for (int i = 0; i < q; i++) {
            st = new StringTokenizer(br.readLine());
            String op = st.nextToken();
            if (op.equals("put")) {
                int key = Integer.parseInt(st.nextToken());
                int value = Integer.parseInt(st.nextToken());
                int ttl = Integer.parseInt(st.nextToken());
                long ts = Long.parseLong(st.nextToken());
                cache.put(key, value, ttl, ts);
            } else {
                int key = Integer.parseInt(st.nextToken());
                long ts = Long.parseLong(st.nextToken());
                System.out.println(cache.get(key, ts));
            }
        }
    }
}
