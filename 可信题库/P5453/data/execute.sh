#!/bin/sh
set -eu

# Java：compile.sh 产出 Main.jar
if [ -f /w/Main.jar ]; then
  exec /usr/bin/java -cp /w/Main.jar Main
fi

# Python 源码（compile.sh: cat template.py >> foo.py）
if [ -f /w/foo.py ]; then
  exec /usr/bin/python3 /w/foo.py
fi

if [ ! -f /w/foo ]; then
  echo "Runtime artifact not found: /w/foo or /w/Main.jar" >&2
  exit 127
fi

# ELF 原生可执行（C/C++/Go/...）必须先于 head：二进制含 NUL，
# 否则 bash 会报 ignored null byte in input
elf_magic="$(LC_ALL=C dd if=/w/foo bs=1 count=4 2>/dev/null | od -An -tx1 | tr -d ' \n')"
if [ "$elf_magic" = "7f454c46" ]; then
  exec /w/foo
fi

# C# / Mono 生成的 PE 文件通常以 MZ 开头
magic="$(LC_ALL=C dd if=/w/foo bs=1 count=2 2>/dev/null | od -An -tx1 | tr -d ' \n')"
if [ "$magic" = "4d5a" ]; then
  exec /usr/bin/mono /w/foo
fi

# 解释型语言：由 compile.sh 在 foo 首行写入固定 shebang 标识（此时文件为文本）
first_line="$(head -n 1 /w/foo 2>/dev/null || true)"

case "$first_line" in
  '#!/usr/bin/node')
    exec /usr/bin/node /w/foo
    ;;
  '#!/usr/bin/python3')
    exec /usr/bin/python3 /w/foo
    ;;
  '#!/usr/bin/pypy3')
    exec /usr/bin/pypy3 /w/foo
    ;;
  '#!/bin/bash')
    exec /bin/bash /w/foo
    ;;
  '#!/usr/bin/php')
    exec /usr/bin/php /w/foo
    ;;
  '#!/usr/bin/ruby')
    exec /usr/bin/ruby /w/foo
    ;;
esac

# 其余视为 Python 字节码（compile.sh 的 py_compile 输出到 /w/foo）
exec /usr/bin/python3 /w/foo
