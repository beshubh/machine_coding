from sortedcontainers import SortedDict, SortedSet
from dataclasses import dataclass


@dataclass(frozen=True)
class LedgerEntry:
    amount: float
    op: str # GRANT | CHARGE
    ts: int
    seq: int

    def __hash__(self):
        return hash(self._sort_key())

    def __eq__(self, other):
        return self._sort_key() == other._sort_key()

    def _sort_key(self):
        return (self.ts, self.seq)

    def __lt__(self, other):
        return self._sort_key() < other._sort_key()


class CreditLedger:

    def __init__(self):
        self.sd = {}

    def get_amount_at_ts(self, seq: int, ts: int, ledger: SortedSet[LedgerEntry]):
        cutoff = LedgerEntry(0, 'GRANT', ts=ts, seq=seq)
        idx = ledger.bisect_left(cutoff)
        candidates = ledger[:idx]
        credit = 0
        for entry in candidates:
            if entry.op == 'GRANT':
                credit += entry.amount
            elif entry.op == 'CHARGE':
                if credit >= entry.amount:
                    credit -= entry.amount
        return credit

    def process(self, requests: list[list[str]]) -> list[int]:
        output = []
        for i, req in enumerate(requests):
            req_type = req[0].strip()
            match req_type.strip():
                case 'GRANT':
                    _, user_id, amount_s, ts_s = req
                    amount = float(amount_s)
                    ts = int(ts_s)
                    entry = LedgerEntry(amount=amount, op='GRANT', ts=ts, seq=i)
                    if user_id not in self.sd:
                        self.sd[user_id] = SortedSet()
                    self.sd[user_id].add(entry)
                case 'CHARGE':
                    _, user_id, amount_s, ts_s = req
                    amount = float(amount_s)
                    ts = int(ts_s)
                    entry = LedgerEntry(amount=amount, op='CHARGE', ts=ts, seq=i)
                    if user_id not in self.sd:
                        self.sd[user_id] = SortedSet()
                    self.sd[user_id].add(entry)

                case 'GET':
                    _, user_id, ts_s = req
                    ts = int(ts_s)
                    if user_id not in self.sd:
                        output.append(0)
                        continue
                    ledger = self.sd[user_id]
                    output.append(self.get_amount_at_ts(i, ts, ledger))
        return output

def solution(requests):
    cl = CreditLedger()
    output = cl.process(requests)
    return output
