import sys
import ast
import os


def load_solution_class():
    if "Solution" in globals():
        return globals()["Solution"]

    candidates = []

    if "__file__" in globals():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidates.append(os.path.join(base_dir, "foo.py"))
        candidates.append(os.path.join(base_dir, "user.py"))

    candidates.append("foo.py")
    candidates.append("user.py")

    for path in candidates:
        if os.path.exists(path):
            namespace = {}
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            exec(code, namespace)
            if "Solution" in namespace:
                return namespace["Solution"]

    try:
        from foo import Solution
        return Solution
    except Exception:
        pass

    try:
        from user import Solution
        return Solution
    except Exception:
        pass

    raise RuntimeError("无法加载 Solution 类")


def parse_input():
    data = sys.stdin.read()
    if not data:
        return ""
    data = data.strip()
    if not data:
        return ""
    try:
        value = ast.literal_eval(data)
        if isinstance(value, str):
            return value
    except Exception:
        pass
    if len(data) >= 2 and data[0] == '"' and data[-1] == '"':
        return data[1:-1]
    return data


def main():
    Solution = load_solution_class()
    instructions = parse_input()
    result = Solution().processInstructions(instructions)
    if result is not None:
        sys.stdout.write(str(result))


if __name__ == "__main__":
    main()
