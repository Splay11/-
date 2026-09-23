class CertAuthority {
    public CertAuthority() {}

    public boolean issue(int certId, int parentId, int expireAt) {
        return false;
    }

    public boolean revoke(int certId) {
        return false;
    }

    public boolean isValid(int certId, int now) {
        return false;
    }

    public int ttl(int certId, int now) {
        return -1;
    }

    public int issuerOf(int certId) {
        return -1;
    }

    public int rootOf(int certId) {
        return -1;
    }
}

public class Solution {}
