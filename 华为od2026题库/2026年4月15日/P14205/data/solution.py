from collections import Counter

class Solution:
    def countKeys(self, s):
        cnt = Counter()
        i = 0
        n = len(s)

        while i < n:
            if i + 1 < n and s[i] == 'u' and s[i + 1] == 'u':
                cnt['j'] += 1
                i += 2
            elif i + 1 < n and s[i] == 't' and s[i + 1] == 't':
                cnt['b'] += 1
                i += 2
            else:
                cnt[s[i]] += 1
                i += 1

        def encode(c):
            if '0' <= c <= '9':
                return ord(c) - ord('0')
            return ord(c) - ord('a') + 10

        arr = sorted(cnt.items(), key=lambda x: (-x[1], x[0]))
        return [[encode(c), v] for c, v in arr]
