# -*- coding: utf-8 -*-
"""生成 data/*.in/*.out；标程语义与题面一致。"""

import ast
from pathlib import Path


def parse_line(line: str):
    comma = line.find(",")
    month = int(line[:comma].strip())
    rest = line[comma + 1 :].strip()
    split_idx = rest.find("],[")
    employees = ast.literal_eval(rest[: split_idx + 1])
    birthdays = ast.literal_eval(rest[split_idx + 2 :])
    return month, employees, birthdays


def expected(month: int, employees: list, birthdays: list) -> int:
    c = 0
    for b in birthdays:
        m = int(b.split("-")[0])
        if m == month:
            c += 1
    return c


CASES = [
    '2,["Alice","Bob"],["02-01","02-28"]',
    '3,["A"],["02-01"]',
    '12,["X"],["12-31"]',
    '1,["Only"],["01-01"]',
    '6,["A","B"],["06-15","07-04"]',
    '2,["Tom,Jr"],["02-29"]',
    '11,["A","B","C"],["11-1","11-02","10-3"]',
    '1,["a","b","c","d"],["01-01","01-02","12-01","01-04"]',
]


def main() -> None:
    data = Path(__file__).resolve().parent / "data"
    data.mkdir(parents=True, exist_ok=True)
    for i, line in enumerate(CASES, start=1):
        month, employees, birthdays = parse_line(line)
        want = expected(month, employees, birthdays)
        inp = data / f"{i}.in"
        outp = data / f"{i}.out"
        inp.write_bytes(line.encode("utf-8"))
        with outp.open("w", encoding="utf-8", newline="\n") as f:
            f.write(str(want) + "\n")
    print("ok:", len(CASES), "pairs")


if __name__ == "__main__":
    main()
