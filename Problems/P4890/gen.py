from pathlib import Path
import random


def solve(n_text: str) -> str:
    n = int(n_text)
    return str(n.bit_length() - 1)


def write_case(data_dir: Path, idx: int, n_text: str) -> None:
    (data_dir / f"{idx}.in").write_text(n_text, encoding="utf-8")
    (data_dir / f"{idx}.out").write_text(solve(n_text) + "\n", encoding="utf-8")


def main() -> None:
    rng = random.Random(4890)
    data_dir = Path(__file__).resolve().parent / "data"
    data_dir.mkdir(exist_ok=True)

    cases = [
        ("5", "样例测试：覆盖题面样例，答案为 2。"),
        ("1", "边界测试：最小正整数，答案为 0。"),
        ("2", "边界测试：刚好是 2 的 1 次幂。"),
        ("3", "边界测试：刚好小于 2 的 2 次幂，卡 k+1 判断。"),
        (str((1 << 20) - 1), "构造测试：刚好小于 2 的 20 次幂，卡 off-by-one。"),
        (str(1 << 20), "构造测试：刚好等于 2 的 20 次幂。"),
        (str(rng.randrange(10**50, 10**51)), "随机测试：中等规模非特殊大数。"),
        (str((1 << 100) + 12345), "构造测试：超过常规整数范围，卡 64 位溢出。"),
        (str((1 << 10000) - 1), "大数据：接近 2 的幂但差 1，卡浮点 log2 与边界。"),
        ("1" + "0" * 4000, "大数据：4001 位十进制数，压测大整数读入。"),
    ]

    for idx, (n_text, _) in enumerate(cases, 1):
        write_case(data_dir, idx, n_text)

    readme_lines = [
        "# 数据生成说明",
        "",
        "本题本地数据保证 $N$ 为正整数，十进制表示长度不超过 $4001$ 位。",
        "",
        "| 组别 | 类型 | 目标 |",
        "|---:|---|---|",
    ]
    for idx, (_, desc) in enumerate(cases, 1):
        readme_lines.append(f"| {idx} | {'大数据' if idx >= 9 else '小数据'} | {desc} |")
    readme_lines.extend(
        [
            "",
            "主要针对的错误解法：",
            "",
            "- 使用 `int` / `long long` 读入导致溢出。",
            "- 使用浮点 `log2` 处理超大整数导致精度错误。",
            "- 对 $N=2^t$ 或 $N=2^t-1$ 的边界判断错误。",
        ]
    )
    (data_dir / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")

    # 自校验：重新计算每组输出，确保生成文件一致。
    for idx in range(1, 11):
        n_text = (data_dir / f"{idx}.in").read_text(encoding="utf-8")
        expected = solve(n_text) + "\n"
        actual = (data_dir / f"{idx}.out").read_text(encoding="utf-8")
        if actual != expected:
            raise RuntimeError(f"case {idx} output mismatch")


if __name__ == "__main__":
    main()
