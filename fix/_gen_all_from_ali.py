# -*- coding: utf-8 -*-
"""从 阿里机考题库 文件夹爬取所有 P#### 目录名，写入 fix/all.txt"""
import os
import re
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

root = '阿里机考题库'
pids = set()
for dirpath, dirs, files in os.walk(root):
    for d in dirs:
        m = re.fullmatch(r'P\d+', d)
        if m:
            pids.add(m.group(0))

sorted_pids = sorted(pids, key=lambda x: int(x[1:]))
with open('fix/all.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(sorted_pids) + '\n')

print('题库PID总数: %d' % len(sorted_pids))
print('已写入 fix/all.txt')
