#!/bin/bash

set -e
if [ $HYDRO_LANG = "py.py3" ]; then
  cat template.py >> foo.py
  python3 -c "import py_compile; py_compile.compile('/w/foo.py', '/w/foo', doraise=True)"

elif [ $HYDRO_LANG = "py" ]; then
  cat template.py >> foo.py
  python -c "import py_compile; py_compile.compile('/w/foo.py', '/w/foo', doraise=True)"

elif [ $HYDRO_LANG = "py.pypy3" ]; then
  cat template.py >> foo.py
  /bin/bash -c "/usr/bin/pypy3 -c \"import py_compile; py_compile.compile('/w/foo.py', '/w/foo', doraise=True)\" && mv foo.py foo"

elif [ $HYDRO_LANG = "java" ]; then
  mv Main.java Solution.java
  mv template.java Main.java
  javac -d /w -encoding utf8 ./Main.java ./Solution.java
  jar cvf Main.jar *.class >/dev/null

elif [ $HYDRO_LANG = "cc.cc98" ]; then
  g++ -x c++ template.cc -o foo -lm -fno-stack-limit -fdiagnostics-color=always -std=c++98 -I/include

elif [ $HYDRO_LANG = "cc.cc98o2" ]; then
  g++ -x c++ template.cc -o foo -lm -fno-stack-limit -fdiagnostics-color=always -std=c++98 -O2 -I/include

elif [ $HYDRO_LANG = "cc.cc11" ]; then
  g++ -x c++ template.cc -o foo -lm -fno-stack-limit -fdiagnostics-color=always -std=c++11 -I/include

elif [ $HYDRO_LANG = "cc.cc11o2" ]; then
  g++ -x c++ template.cc -o foo -lm -fno-stack-limit -fdiagnostics-color=always -std=c++11 -O2 -I/include

elif [ $HYDRO_LANG = "cc.cc14" ]; then
  g++ -x c++ template.cc -o foo -lm -fno-stack-limit -fdiagnostics-color=always -std=c++14 -I/include

elif [ $HYDRO_LANG = "cc.cc14o2" ]; then
  g++ -x c++ template.cc -o foo -lm -fno-stack-limit -fdiagnostics-color=always -std=c++14 -O2 -I/include

elif [ $HYDRO_LANG = "cc.cc17" ]; then
  g++ -x c++ template.cc -o foo -lm -fno-stack-limit -fdiagnostics-color=always -std=c++17 -I/include

elif [ $HYDRO_LANG = "cc.cc17o2" ]; then
  g++ -x c++ template.cc -o foo -lm -fno-stack-limit -fdiagnostics-color=always -std=c++17 -O2 -I/include

elif [ $HYDRO_LANG = "cc" ]; then
  g++ -x c++ template.cc -o foo -lm -fno-stack-limit -fdiagnostics-color=always -std=c++14 -I/include

elif [ $HYDRO_LANG = "c" ]; then
  gcc template.c -o foo -lm -std=c99

elif [ $HYDRO_LANG = "pas" ]; then
  fpc -O2 -o/w/foo template.pas

elif [ $HYDRO_LANG = "go" ]; then
  env GOMAXPROCS=1 go build -o foo template.go

elif [ $HYDRO_LANG = "rs" ]; then
  rustc -O -o /w/foo /w/template.rs

elif [ $HYDRO_LANG = "hs" ]; then
  ghc -O -outputdir /tmp -o foo template.hs

elif [ $HYDRO_LANG = "cs" ]; then
  mcs -optimize+ -out:/w/foo /w/template.cs

elif [ $HYDRO_LANG = "bash" ]; then
  :
elif [ $HYDRO_LANG = "php" ]; then
  :
elif [ $HYDRO_LANG = "js" ]; then
  :
elif [ $HYDRO_LANG = "rb" ]; then
  :
else
  echo "Unsupported language: $HYDRO_LANG" >&2
  exit 1
fi
