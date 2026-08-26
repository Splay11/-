# 思路: 模拟

用 8 个方向偏移量来考虑给定坐标可以到达的上下左右和两条对角线的位置

注意输出的时候按照字典序大小输出可达的所有位置

# 代码
```python
s = input()
cy, cx = ord(s[0]) - ord('a'), int(s[1]) - 1
n, m = 8, 8

s = set()
dx = [-1, -1, -1, 0, 1, 1, 1, 0]
dy = [-1, 0, 1, 1, 1, 0, -1, -1]

for i in range(8):
    x, y = cx, cy
    while 0 <= x < 8 and 0 <= y < 8:
        nx = x + dx[i]
        ny = y + dy[i]
        if 0 <= nx < 8 and 0 <= ny < 8:
            s.add((nx, ny))
        x, y = nx, ny

lst = list(s)
lst.sort(key=lambda t: (t[1], t[0]))

length = len(lst)
print(length)
for i in range(length):
    print(f'{chr(lst[i][1] + ord("a"))}{lst[i][0] + 1}', end='\n' if i + 1 == length else ' ')
```