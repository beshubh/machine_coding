from dataclasses import dataclass


@dataclass
class TransactionEvent:
    latest_timestamp: int
    observed_status: str
    has_conflict: bool



class PaymentEventReconcilation:

    def __init__(self) -> None:
       self._transactions: dict[str, TransactionEvent] = {}


    def process_transaction(self, tid: str, ts: int, status: str) -> None:
        entry = self._transactions.get(tid)
        if entry is None:
            self._transactions[tid] = TransactionEvent(latest_timestamp=ts, observed_status=status, has_conflict=False)
            return
        if entry.latest_timestamp == ts and entry.observed_status == status:
            # same ts and status, so ignore
            return
        elif entry.latest_timestamp == ts:
            # same ts but different status, need review
            entry.has_conflict = True
        elif entry.latest_timestamp < ts:
            # greater ts, so override all values with the latest
            entry.has_conflict = False
            entry.observed_status = status
            entry.latest_timestamp = ts

    def process(self, transactions: list[str]) -> list[str]:
        result = []
        for transaction in transactions:
            tid, ts, status = transaction.split(',')
            ts = int(ts)
            self.process_transaction(tid, ts, status)

        for k in self._transactions.keys():
            entry = self._transactions[k]
            if entry.has_conflict:
                result.append(f'{k},needs_review')
            else:
                result.append(f'{k},{entry.observed_status}')
        return result
