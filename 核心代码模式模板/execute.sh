#!/bin/sh
set -eu

# Java：你的 compile.sh 产出 Main.jar
if [ -f /w/Main.jar ]; then
  exec /usr/bin/java -cp /w/Main.jar Main
fi

if [ ! -f /w/foo ]; then
  echo "Runtime artifact not found: /w/foo or /w/Main.jar" >&2
  exit 127
fi

# 解释型语言：由 compile.sh 在 foo 首行写入固定 shebang 标识
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

# C# / Mono 生成的 PE 文件通常以 MZ 开头
magic="$(LC_ALL=C dd if=/w/foo bs=1 count=2 2>/dev/null | od -An -tx1 | tr -d ' \n')"
if [ "$magic" = "4d5a" ]; then
  exec /usr/bin/mono /w/foo
fi

# C / C++ / Go / Rust / Pascal / Haskell 等原生可执行文件
exec /w/foo
