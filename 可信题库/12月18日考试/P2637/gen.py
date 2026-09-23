#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2637 微服务管理 — 造数脚本（stdin 形态与题面样例一致）。"""

from __future__ import annotations

import random
from pathlib import Path
from typing import Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SEED = 2637
N_CASES = 10


class ServiceMgrSys:
    def __init__(self):
        self.running: Dict[str, Set[int]] = {}
        self.on_server: Dict[int, Set[str]] = {}
        self.deps: Dict[str, Set[str]] = {}

    def rebootServers(self, serverIds: List[int]) -> None:
        for sid in serverIds:
            for name in list(self.on_server.get(sid, set())):
                self.running[name].discard(sid)
                if not self.running[name]:
                    del self.running[name]
            self.on_server[sid] = set()

    def startService(self, serverId: int, serviceName: str) -> bool:
        if serviceName in self.on_server.get(serverId, set()):
            return False
        self.on_server.setdefault(serverId, set()).add(serviceName)
        self.running.setdefault(serviceName, set()).add(serverId)
        return True

    def addDependency(self, fromServiceName: str, toServiceName: str) -> bool:
        if toServiceName in self.deps.get(fromServiceName, set()):
            return False
        self.deps.setdefault(fromServiceName, set()).add(toServiceName)
        return True

    def isServiceAvailable(self, serviceName: str) -> bool:
        memo: Dict[str, bool] = {}

        def dfs(name: str) -> bool:
            if name in memo:
                return memo[name]
            if name not in self.running or not self.running[name]:
                memo[name] = False
                return False
            for dep in self.deps.get(name, set()):
                if not dfs(dep):
                    memo[name] = False
                    return False
            memo[name] = True
            return True

        return dfs(serviceName)


def simulate(lines: List[str]) -> List[str]:
    sys = ServiceMgrSys()
    out = ["null"]
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        if line.startswith("startService"):
            inner = line[line.find("(") + 1 : line.rfind(")")]
            a, b = inner.split(",", 1)
            ok = sys.startService(int(a.strip()), b.strip().strip('"'))
            out.append("true" if ok else "false")
        elif line.startswith("addDependency"):
            inner = line[line.find("(") + 1 : line.rfind(")")]
            a, b = inner.split(",", 1)
            ok = sys.addDependency(a.strip().strip('"'), b.strip().strip('"'))
            out.append("true" if ok else "false")
        elif line.startswith("isServiceAvailable"):
            inner = line[line.find("(") + 1 : line.rfind(")")]
            ok = sys.isServiceAvailable(inner.strip().strip('"'))
            out.append("true" if ok else "false")
        elif line.startswith("rebootServers"):
            inner = line[line.find("[") + 1 : line.find("]")]
            ids = [int(x.strip()) for x in inner.split(",") if x.strip()]
            sys.rebootServers(ids)
            out.append("null")
    return out


def write_in(path: Path, lines: List[str]) -> None:
    # .in：最后一行后不要换行
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, lines: List[str]) -> None:
    # .out：末尾有且仅有一个 \n
    path.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def fmt_reboot(ids: List[int]) -> str:
    return "rebootServers([" + ", ".join(str(x) for x in ids) + "])"


def sample_case() -> List[str]:
    return [
        "ServiceMgrSys()",
        'startService(1, "serviceA")',
        'startService(2, "serviceA")',
        'startService(2, "serviceA")',
        'addDependency("serviceB", "serviceA")',
        "rebootServers([2])",
        'isServiceAvailable("serviceA")',
        'startService(2, "serviceB")',
        'isServiceAvailable("serviceB")',
        "rebootServers([2, 1])",
        'isServiceAvailable("serviceA")',
        'startService(1, "serviceA")',
        'isServiceAvailable("serviceA")',
    ]


def hack_multi_instance() -> List[str]:
    # 卡：重启一台后误判服务不可用（忽略其它实例）
    return [
        "ServiceMgrSys()",
        'startService(1, "A")',
        'startService(2, "A")',
        "rebootServers([1])",
        'isServiceAvailable("A")',
        "rebootServers([2])",
        'isServiceAvailable("A")',
    ]


def hack_transitive_dep() -> List[str]:
    # 卡：只检查依赖是否在运行，不递归检查「可提供服务」
    return [
        "ServiceMgrSys()",
        'startService(1, "C")',
        'startService(1, "B")',
        'startService(1, "A")',
        'addDependency("B", "C")',
        'addDependency("A", "B")',
        'isServiceAvailable("A")',
        "rebootServers([1])",
        'startService(2, "B")',
        'startService(2, "A")',
        'isServiceAvailable("B")',  # C 无实例 → false
        'isServiceAvailable("A")',  # B 不可用 → false
        'startService(2, "C")',
        'isServiceAvailable("A")',  # true
    ]


def hack_duplicate_and_no_self() -> List[str]:
    # 卡：重复 start/依赖；以及「依赖可用但自身未启动」误判 true
    return [
        "ServiceMgrSys()",
        'startService(3, "base")',
        'addDependency("top", "base")',
        'addDependency("top", "base")',
        'isServiceAvailable("top")',
        'startService(3, "top")',
        'startService(3, "top")',
        'isServiceAvailable("top")',
        "rebootServers([3])",
        'isServiceAvailable("base")',
        'isServiceAvailable("top")',
    ]


def chain_case(depth: int, sid: int = 1) -> List[str]:
    # 构造：长依赖链 S0 <- S1 <- ... <- S{depth-1}
    lines = ["ServiceMgrSys()"]
    names = [f"S{i}" for i in range(depth)]
    for i in range(depth - 1):
        lines.append(f'addDependency("{names[i + 1]}", "{names[i]}")')
    for name in names:
        lines.append(f'startService({sid}, "{name}")')
    lines.append(f'isServiceAvailable("{names[-1]}")')
    lines.append(fmt_reboot([sid]))
    lines.append(f'isServiceAvailable("{names[-1]}")')
    # 只重启后重开底层，上层仍不可用
    lines.append(f'startService({sid}, "{names[0]}")')
    lines.append(f'isServiceAvailable("{names[1]}")')
    return lines


def random_case(rng: random.Random, n_ops: int, n_servers: int, n_services: int) -> List[str]:
    services = [f"svc{i}" for i in range(n_services)]
    # 拓扑序：i 只能依赖 j < i，保证无环
    edges: Set[Tuple[str, str]] = set()
    lines = ["ServiceMgrSys()"]
    ops_left = n_ops - 1

    def maybe_query():
        nonlocal ops_left
        if ops_left <= 0:
            return
        name = rng.choice(services)
        lines.append(f'isServiceAvailable("{name}")')
        ops_left -= 1

    while ops_left > 0:
        kind = rng.random()
        if kind < 0.35 and ops_left > 0:
            sid = rng.randint(0, n_servers - 1)
            name = rng.choice(services)
            lines.append(f'startService({sid}, "{name}")')
            ops_left -= 1
            if rng.random() < 0.3:
                maybe_query()
        elif kind < 0.55 and ops_left > 0:
            # 添加依赖：from 下标更大
            i = rng.randint(1, n_services - 1)
            j = rng.randint(0, i - 1)
            a, b = services[i], services[j]
            lines.append(f'addDependency("{a}", "{b}")')
            edges.add((a, b))
            ops_left -= 1
        elif kind < 0.75 and ops_left > 0:
            k = rng.randint(1, min(500, n_servers))
            ids = rng.sample(range(n_servers), k)
            lines.append(fmt_reboot(ids))
            ops_left -= 1
        else:
            maybe_query()
            if ops_left > 0 and rng.random() < 0.5:
                # 再查一次不同服务
                maybe_query()
    return lines


def large_pressure(rng: random.Random) -> List[str]:
    # 接近 1000 次调用：多服务器、多服务、长链 + 批量重启
    n_servers = 501  # serverId 0..500
    n_services = 80
    services = [f"s{i}" for i in range(n_services)]
    lines = ["ServiceMgrSys()"]
    # 链式依赖 0<-1<-...<-79
    for i in range(n_services - 1):
        lines.append(f'addDependency("{services[i + 1]}", "{services[i]}")')
    # 每个服务部署到多台服务器
    for i, name in enumerate(services):
        for t in range(3):
            sid = (i * 3 + t) % n_servers
            lines.append(f'startService({sid}, "{name}")')
    lines.append(f'isServiceAvailable("{services[-1]}")')
    # 大重启
    ids = list(range(0, n_servers, 2))
    # 分批，避免单次数组超 500：题面 serverIds.length <= 500
    for i in range(0, len(ids), 500):
        chunk = ids[i : i + 500]
        lines.append(fmt_reboot(chunk))
    lines.append(f'isServiceAvailable("{services[-1]}")')
    # 恢复底层若干层
    for i in range(0, 20):
        lines.append(f'startService({i}, "{services[i]}")')
    lines.append(f'isServiceAvailable("{services[19]}")')
    lines.append(f'isServiceAvailable("{services[20]}")')
    # 补随机操作直到接近上限
    while len(lines) < 980:
        if rng.random() < 0.5:
            sid = rng.randint(0, n_servers - 1)
            name = rng.choice(services)
            lines.append(f'startService({sid}, "{name}")')
        else:
            name = rng.choice(services)
            lines.append(f'isServiceAvailable("{name}")')
    # 再加一次大查询与重启
    lines.append(fmt_reboot(list(range(0, 500))))
    lines.append(f'isServiceAvailable("{services[0]}")')
    assert len(lines) <= 1000
    return lines


def build_cases(rng: random.Random) -> List[List[str]]:
    cases: List[List[str]] = []
    # 1 样例
    cases.append(sample_case())
    # 2 基础：单服务无依赖
    cases.append(
        [
            "ServiceMgrSys()",
            'isServiceAvailable("x")',
            'startService(0, "x")',
            'isServiceAvailable("x")',
            "rebootServers([0])",
            'isServiceAvailable("x")',
        ]
    )
    # 3 hack 多实例
    cases.append(hack_multi_instance())
    # 4 hack 传递依赖
    cases.append(hack_transitive_dep())
    # 5 hack 重复与自身未启动
    cases.append(hack_duplicate_and_no_self())
    # 6 边界：最小服务器 id、短名字、单元素重启
    cases.append(
        [
            "ServiceMgrSys()",
            'startService(0, "a")',
            'startService(1000, "b")',
            'addDependency("b", "a")',
            'isServiceAvailable("b")',
            "rebootServers([0])",
            'isServiceAvailable("b")',
            'startService(1000, "a")',
            'isServiceAvailable("b")',
        ]
    )
    # 7 中等随机
    cases.append(random_case(rng, n_ops=80, n_servers=20, n_services=12))
    # 8 构造长链（中小）
    cases.append(chain_case(15, sid=7))
    # 9 大：接近调用上限
    cases.append(large_pressure(rng))
    # 10 大：宽依赖（多扇入）+ 大批量重启
    services = [f"w{i}" for i in range(40)]
    lines = ["ServiceMgrSys()"]
    for i in range(1, 40):
        # 每个依赖前一个与前两个（若有）
        lines.append(f'addDependency("{services[i]}", "{services[i - 1]}")')
        if i >= 2:
            lines.append(f'addDependency("{services[i]}", "{services[i - 2]}")')
    for i, name in enumerate(services):
        lines.append(f'startService({i}, "{name}")')
        lines.append(f'startService({i + 40}, "{name}")')
    lines.append(f'isServiceAvailable("{services[-1]}")')
    lines.append(fmt_reboot(list(range(0, 40))))
    lines.append(f'isServiceAvailable("{services[-1]}")')  # 仍有第二实例
    lines.append(fmt_reboot(list(range(40, 80))))
    lines.append(f'isServiceAvailable("{services[-1]}")')
    while len(lines) < 900:
        lines.append(f'isServiceAvailable("{rng.choice(services)}")')
        if len(lines) < 900:
            sid = rng.randint(0, 200)
            lines.append(f'startService({sid}, "{rng.choice(services)}")')
    cases.append(lines)
    assert len(cases) == N_CASES
    return cases


def write_config(n: int) -> None:
    lines = [
        "type: default",
        "user_extra_files:",
        "  - template.py",
        "  - template.java",
        "  - template.cc",
        "  - compile.sh",
        "  - config.yaml",
        "subtasks:",
        "  - score: 100",
        "    if: []",
        "    id: 1",
        "    type: sum",
        "    cases:",
    ]
    for i in range(1, n + 1):
        lines.append(f"      - input: {i}.in")
        lines.append(f"        output: {i}.out")
    lines.extend(
        [
            "langs:",
            "  - py.py3",
            "  - java",
            "  - cc.cc14o2",
            "  - py",
            "  - cc",
        ]
    )
    (DATA / "config.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rng = random.Random(SEED)
    DATA.mkdir(parents=True, exist_ok=True)
    # 清理旧测例
    for p in DATA.glob("*.in"):
        p.unlink()
    for p in DATA.glob("*.out"):
        p.unlink()

    cases = build_cases(rng)
    for idx, lines in enumerate(cases, 1):
        assert 1 <= len(lines) <= 1000
        out_lines = simulate(lines)
        write_in(DATA / f"{idx}.in", lines)
        write_out(DATA / f"{idx}.out", out_lines)
        # 自校验
        again = simulate(lines)
        if again != out_lines:
            raise SystemExit(f"自校验失败: case {idx}")

    write_config(N_CASES)

    # 换行规则检查
    for i in range(1, N_CASES + 1):
        raw_in = (DATA / f"{i}.in").read_bytes()
        raw_out = (DATA / f"{i}.out").read_bytes()
        if raw_in.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾不应有换行")
        if not raw_out.endswith(b"\n") or raw_out.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 末尾换行不符合规则")

    print(f"OK: generated {N_CASES} cases into {DATA}")


if __name__ == "__main__":
    main()
