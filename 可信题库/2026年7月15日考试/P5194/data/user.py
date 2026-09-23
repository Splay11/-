class LogSystem:
    def __init__(self):
        pass

    def enter(self, spanId: int, inherit: bool) -> None:
        pass

    def log(self, msg: str) -> str:
        return ""

    def leave(self, spanId: int) -> None:
        pass
