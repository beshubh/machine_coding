from dataclasses import dataclass


@dataclass
class TokenEntry:
    exp: int


class AuthenticationManager:
    def __init__(self, timeToLive: int):
        self._ttl = timeToLive
        self._s: dict[str, TokenEntry] = {}

    def generate(self, tokenId: str, currentTime: int) -> None:
        self._s[tokenId] = TokenEntry(exp=currentTime + self._ttl)

    def renew(self, tokenId: str, currentTime: int) -> None:
        token_entry = self._s.get(tokenId)
        if token_entry is None:
            return
        if token_entry.exp <= currentTime:
            return
        token_entry.exp = currentTime + self._ttl

    def countUnexpiredTokens(self, currentTime: int) -> int:
        count = 0
        for tokenId in self._s:
            if self._s[tokenId].exp <= currentTime:
                continue
            count += 1
        return count


# Your AuthenticationManager object will be instantiated and called as such:
# obj = AuthenticationManager(timeToLive)
# obj.generate(tokenId,currentTime)
# obj.renew(tokenId,currentTime)
# param_3 = obj.countUnexpiredTokens(currentTime)
