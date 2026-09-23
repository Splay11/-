#!/bin/sh
set -eu

# Java
if [ -f /w/Main.jar ]; then
  exec /usr/bin/java -cp /w/Main.jar Main
fi

# 没有运行产物时静默退出
if [ ! -f /w/foo ]; then
  exit 127
fi

# 读取前两个字节，避免把二进制文件当文本读
magic="$(LC_ALL=C dd if=/w/foo bs=1 count=2 2>/dev/null | od -An -tx1 | tr -d ' \n')"

# 解释型语言：只有以 #! 开头时才读取第一行
if [ "$magic" = "2321" ]; then
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
fi

# C# / Mono
if [ "$magic" = "4d5a" ]; then
  exec /usr/bin/mono /w/foo
fi

# 原生可执行文件
exec /w/foo
