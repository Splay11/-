# -*- coding: utf-8 -*-


class Solution:
  def processExpression(self, inputStr: str) -> str:
    s = inputStr
    if len(s) > 10000:
      return '"NA"'
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-")
    for ch in s:
      if ch not in allowed:
        return '"NA"'
    if not s:
      return '"NA"'

    pos = 0

    def parse_number():
      nonlocal pos
      n = len(s)
      if pos >= n:
        return False, 0
      start = pos
      if s[pos] == "0" and pos + 1 < n and s[pos + 1] in "xX":
        pos += 2
        val = 0
        ok = False
        while pos < n:
          c = s[pos]
          if c.isdigit():
            d = ord(c) - ord("0")
          elif "a" <= c <= "f":
            d = ord(c) - ord("a") + 10
          elif "A" <= c <= "F":
            d = ord(c) - ord("A") + 10
          else:
            break
          ok = True
          val = val * 16 + d
          pos += 1
        if not ok:
          return False, 0
        if val > 999:
          return False, 0
        return True, val
      if s[pos] == "0" and pos + 1 < n and s[pos + 1] in "oO":
        pos += 2
        val = 0
        ok = False
        while pos < n and "0" <= s[pos] <= "7":
          ok = True
          val = val * 8 + (ord(s[pos]) - ord("0"))
          pos += 1
        if not ok:
          return False, 0
        if val > 999:
          return False, 0
        return True, val
      if not s[pos].isdigit():
        return False, 0
      val = 0
      while pos < n and s[pos].isdigit():
        val = val * 10 + (ord(s[pos]) - ord("0"))
        pos += 1
      if val > 999:
        return False, 0
      return True, val

    ok, result = parse_number()
    if not ok:
      return '"NA"'
    while pos < len(s):
      op = s[pos]
      if op not in "+-":
        return '"NA"'
      pos += 1
      ok, val = parse_number()
      if not ok:
        return '"NA"'
      if op == "+":
        result += val
      else:
        result -= val
    if pos != len(s):
      return '"NA"'
    if result > 255:
      result = 255
    elif result < -255:
      result = -255
    out = (~result) & 0xFF
    return '"0x%02X"' % out
