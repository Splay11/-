class Solution:
    def firstTasteLevel(self, note: str) -> int:
        for ch in note:
            if "0" <= ch <= "9":
                return ord(ch) - ord("0")
        return -1
