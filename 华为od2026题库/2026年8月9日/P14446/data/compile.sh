#!/bin/bash
set -euo pipefail

cd /w

make_script() {
  local shebang="$1"
  local source_file="$2"
  local template_file="${3-}"

  {
    printf '%s\n' "$shebang"
    cat "$source_file"

    if [ -n "$template_file" ]; then
      printf '\n'
      cat "$template_file"
    fi

    printf '\n'
  } > foo

  chmod 755 foo
}

case "${HYDRO_LANG:-}" in
  py.py3)
    make_script '#!/usr/bin/python3' 'foo.py' 'template.py'
    /usr/bin/python3 -m py_compile foo
    ;;

  py)
    make_script '#!/usr/bin/python' 'foo.py' 'template.py'
    /usr/bin/python -m py_compile foo
    ;;

  py.pypy3)
    make_script '#!/usr/bin/pypy3' 'foo.py' 'template.py'
    /usr/bin/pypy3 -m py_compile foo
    ;;

  java)
    mv Main.java Solution.java
    mv template.java Main.java

    javac -d /w -encoding utf8 /w/Main.java /w/Solution.java

    rm -f /w/Main.jar /w/foo
    jar cf /w/Main.jar -C /w .
    cp /w/Main.jar /w/foo
    ;;

  cc.cc98)
    g++ -x c++ template.cc -o foo -lm -fno-stack-limit \
      -fdiagnostics-color=always -std=c++98 -I/include
    ;;

  cc.cc98o2)
    g++ -x c++ template.cc -o foo -lm -fno-stack-limit \
      -fdiagnostics-color=always -std=c++98 -O2 -I/include
    ;;

  cc.cc11)
    g++ -x c++ template.cc -o foo -lm -fno-stack-limit \
      -fdiagnostics-color=always -std=c++11 -I/include
    ;;

  cc.cc11o2)
    g++ -x c++ template.cc -o foo -lm -fno-stack-limit \
      -fdiagnostics-color=always -std=c++11 -O2 -I/include
    ;;

  cc.cc14)
    g++ -x c++ template.cc -o foo -lm -fno-stack-limit \
      -fdiagnostics-color=always -std=c++14 -I/include
    ;;

  cc.cc14o2)
    g++ -x c++ template.cc -o foo -lm -fno-stack-limit \
      -fdiagnostics-color=always -std=c++14 -O2 -I/include
    ;;

  cc.cc17)
    g++ -x c++ template.cc -o foo -lm -fno-stack-limit \
      -fdiagnostics-color=always -std=c++17 -I/include
    ;;

  cc.cc17o2)
    g++ -x c++ template.cc -o foo -lm -fno-stack-limit \
      -fdiagnostics-color=always -std=c++17 -O2 -I/include
    ;;

  cc)
    g++ -x c++ template.cc -o foo -lm -fno-stack-limit \
      -fdiagnostics-color=always -std=c++14 -I/include
    ;;

  c)
    gcc -x c template.c -o foo -lm -fno-stack-limit \
      -fdiagnostics-color=always -std=c11 -I/include
    ;;

  go)
    env GOMAXPROCS=1 go build -o /w/foo /w/template.go
    ;;

  js)
    # 用户 foo.js 在前，template.js 在后。
    make_script '#!/usr/bin/node' 'foo.js' 'template.js'
    /usr/bin/node --check /w/foo
    ;;

  *)
    echo "Unsupported language: ${HYDRO_LANG:-<empty>}" >&2
    exit 1
    ;;
esac
