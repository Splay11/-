# -*- coding: utf-8 -*-
import os, re, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

root = '阿里机考题库'
pids = set()
for dirpath, dirs, files in os.walk(root):
    for d in dirs:
        m = re.fullmatch(r'P\d+', d)
        if m:
            pids.add(m.group(0))

allp = [l.strip() for l in open('fix/all.txt', encoding='utf-8') if l.strip()]
allset = set(allp)

out = []
out.append('题库PID总数:%d' % len(pids))
out.append('all.txt总数:%d' % len(allp))
out.append('在题库但不在all.txt:' + ','.join(sorted(pids - allset)))
out.append('在all.txt但不在题库:' + ','.join(sorted(allset - pids)))
open('fix/_pid_compare.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done')
