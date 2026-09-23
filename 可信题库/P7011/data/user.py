class CertAuthority:
    def __init__(self):
        pass

    def issue(self, certId: int, parentId: int, expireAt: int) -> bool:
        return False

    def revoke(self, certId: int) -> bool:
        return False

    def isValid(self, certId: int, now: int) -> bool:
        return False

    def ttl(self, certId: int, now: int) -> int:
        return -1

    def issuerOf(self, certId: int) -> int:
        return -1

    def rootOf(self, certId: int) -> int:
        return -1
