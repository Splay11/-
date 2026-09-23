# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(526120260820)


def run_std(text):
    r = subprocess.run([sys.executable, str(ROOT / "std.py")], input=text.encode(), capture_output=True, check=True)
    return r.stdout.decode()


def write_pair(idx, tin, tout):
    DATA.mkdir(parents=True, exist_ok=True)
    if tin.endswith("\n"):
        raise RuntimeError("in trailing nl")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError("out nl")
    (DATA / f"{idx}.in").write_bytes(tin.encode())
    (DATA / f"{idx}.out").write_bytes(tout.encode())


def fmt(plans, logs):
    lines = [f"{len(plans)} {len(logs)}"]
    for p in plans:
        lines.append(" ".join(p))
    for lg in logs:
        lines.append(" ".join(lg))
    return "\n".join(lines)


def main():
    cases = []
    cases.append(fmt(
        [["pkg_a", "scene1", "v1.0"], ["pkg_b", "scene1", "v1.0"], ["pkg_c", "scene2", "v2.0"]],
        [
            ["pkg_a", "v1.0", "android", "READY"],
            ["pkg_a", "v1.0", "ios", "READY"],
            ["pkg_a", "v1.0", "pc", "READY"],
            ["pkg_b", "v1.0", "android", "READY"],
            ["pkg_b", "v1.0", "ios", "FAIL"],
            ["pkg_b", "v1.0", "pc", "READY"],
            ["pkg_c", "v1.5", "android", "READY"],
        ],
    ))
    cases.append(fmt(
        [["pkg_x", "sceneA", "build-1"], ["pkg_y", "sceneA", "build-1"]],
        [
            ["pkg_x", "build-1", "android", "FAIL"],
            ["pkg_x", "build-1", "android", "READY"],
            ["pkg_x", "build-1", "ios", "READY"],
            ["pkg_x", "build-1", "pc", "READY"],
            ["pkg_y", "build-1", "android", "READY"],
            ["pkg_y", "build-1", "ios", "READY"],
            ["pkg_y", "build-1", "pc", "READY"],
        ],
    ))
    cases.append(fmt([["only", "s", "v1"]], []))
    cases.append(fmt(
        [["a", "s", "1"]],
        [["a", "1", "android", "READY"], ["a", "1", "ios", "READY"], ["a", "1", "pc", "READY"]],
    ))
    # random medium
    plans = [[f"r{i}", f"sc{i%3}", f"v{i%2}"] for i in range(20)]
    logs = []
    for p in plans:
        for plat in ("android", "ios", "pc"):
            if RNG.random() < 0.7:
                logs.append([p[0], p[2], plat, "READY" if RNG.random() < 0.8 else "FAIL"])
    cases.append(fmt(plans, logs))
    cases.append(fmt([["z", "s", "v"]], [["z", "v", "android", "FAIL"]] * 5))
    # larger
    R = 500
    plans = [[f"id_{i}", f"scene_{i%10}", f"ver_{i%5}"] for i in range(R)]
    logs = []
    for i in range(R):
        for plat in ("android", "ios", "pc"):
            if RNG.random() < 0.85:
                logs.append([f"id_{i}", f"ver_{i%5}", plat, "READY"])
            if RNG.random() < 0.1:
                logs.append([f"id_{i}", f"ver_{i%5}", plat, "FAIL"])
    cases.append(fmt(plans, logs))
    cases.append(fmt(
        [[f"p{i}", "s", "v1"] for i in range(100)],
        [[f"p{i}", "v1", plat, "READY"] for i in range(100) for plat in ("android", "ios", "pc")],
    ))
    # near max R
    R = 2000
    plans = [[f"res{i}", f"sc{i}", f"v{i}"] for i in range(R)]
    logs = []
    for i in range(R):
        if i % 3 == 0:
            continue  # all missing
        for plat in ("android", "ios", "pc"):
            if i % 3 == 1 and plat == "ios":
                continue
            logs.append([f"res{i}", f"v{i}", plat, "READY"])
    cases.append(fmt(plans, logs))
    # max-ish
    R = 5000
    plans = [[f"pkg{i}", "main", "v1.0"] for i in range(R)]
    logs = []
    for i in range(R):
        for plat in ("android", "ios", "pc"):
            logs.append([f"pkg{i}", "v1.0", plat, "READY"])
            if RNG.random() < 0.05:
                logs.append([f"pkg{i}", "v1.0", plat, "FAIL"])
    cases.append(fmt(plans, logs[:30000]))

    assert len(cases) == 10
    for i, tin in enumerate(cases, 1):
        tout = run_std(tin)
        if not tout.endswith("\n"):
            tout += "\n"
        write_pair(i, tin, tout)
        print(f"{i} ok {len(tin)}")


if __name__ == "__main__":
    main()
