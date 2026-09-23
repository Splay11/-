class CertAuthority {
 public:
  CertAuthority() {}

  bool issue(int certId, int parentId, int expireAt) {
    (void)certId;
    (void)parentId;
    (void)expireAt;
    return false;
  }

  bool revoke(int certId) {
    (void)certId;
    return false;
  }

  bool isValid(int certId, int now) {
    (void)certId;
    (void)now;
    return false;
  }

  int ttl(int certId, int now) {
    (void)certId;
    (void)now;
    return -1;
  }

  int issuerOf(int certId) {
    (void)certId;
    return -1;
  }

  int rootOf(int certId) {
    (void)certId;
    return -1;
  }
};
