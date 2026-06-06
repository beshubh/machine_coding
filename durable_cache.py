from typing import Any
from dataclasses import dataclass

import threading
import time
import os
import queue
import zlib

from pathlib import Path

@dataclass
class CacheRecord:
    op: str # put | del
    key: str
    value: str
    done: threading.Event
    error: BaseException | None = None


class DCache:

    def __init__(
        self,
        path: str | Path = "__wal",
        max_batch_size: int = 150,
        max_batch_delay: float = 0.001
    ) -> None:
        self._store: dict[str, str] = {}
        self._path = path
        self._max_batch_size = max_batch_size
        self._max_batch_delay = max_batch_delay
        self._lock = threading.RLock()
        self._close_lock = threading.Lock()
        self._closed = False
        self._recover()

        self._thread = threading.Thread(target=self._worker)
        self._q = queue.Queue()
        self._walfile = open(path, mode='a')
        self._thread.start()

    def _recover(self):
        path = Path(self._path)
        path.touch()
        with open(path, mode='rb+') as f:
            good_offset = 0
            recovered_store: dict[str, str] = {}
            while True:
                start = f.tell()
                header = f.readline()
                if not header:
                    break
                try:
                    keylens, valuelens, kcss, vcss = header.decode().strip().split()
                    keylen = int(keylens)
                    valuelen = int(valuelens)
                    kcs = int(kcss)
                    vcs = int(vcss)
                except (ValueError, TypeError):
                    break

                key = f.read(keylen)
                if len(key) != keylen:
                    print('key len mismatchs')
                    break
                value = f.read(valuelen)
                if len(value) != valuelen:
                    print('value len mismatch')
                    break
                newline = f.read(1)
                if newline != b'\n':
                    print('no new line at the end')
                    break

                actual_checksum_key = zlib.crc32(key)
                if actual_checksum_key != kcs:
                    print('key checksum mismatch')
                    break

                actual_checksum_val = zlib.crc32(value)
                if actual_checksum_val != vcs:
                    print('value checksum mismatch')
                    break

                key_str = key.decode('utf-8')
                value_str = value.decode('utf-8')
                if value_str == '':
                    recovered_store.pop(key_str, None)
                else:
                    recovered_store[key_str] = value_str

                good_offset = f.tell()
            self._store.update(recovered_store)
            f.truncate(good_offset)

    def _encode(self, cache_record: CacheRecord) -> tuple[bytes, bytes]:
        """
        Encodes `CacheRecord` as
        header: |keylen| |valuelen| keychecksum valuechecksum\n
        payload: |key| |value|\n

        returns header and pyload as bytes
        """
        keyb = cache_record.key.encode('utf-8')
        keylen = len(keyb)
        keychecksum = zlib.crc32(keyb)
        valueb = cache_record.value.encode('utf-8')
        valuelen = len(valueb)
        valuechecksum = zlib.crc32(valueb)
        header = f'{keylen} {valuelen} {keychecksum} {valuechecksum}\n'.encode('utf-8')
        payload = keyb + valueb + b'\n'
        return (header, payload)


    def close(self) -> None:
        with self._close_lock:
            self._closed = True
            self._q.put(None) # send sentinel to tell consumer to stop
        self._thread.join()

    def put(self, key: str, value: str) -> None:
        cache_record = CacheRecord(op='put', key=key,value=value, done=threading.Event())
        with self._close_lock: # assume read lock here so put can have multiple of these
            if self._closed:
                raise RuntimeError("Cache is closed")
            self._q.put(cache_record)
            # wait for the successful callback
        cache_record.done.wait()
        if cache_record.error is not None:
            raise cache_record.error

    def get(self, key: str) -> str | None:
        with self._lock:
            value = self._store.get(key)
            if value and len(value) == 0:
                return None
            return value

    def delete(self, key: str) -> None:
        with self._close_lock:
            if self._closed:
                raise RuntimeError('Cache closed')
            cache_record = CacheRecord(op='del', key=key,value='', done=threading.Event())
            self._q.put(cache_record)
        cache_record.done.wait()
        if cache_record.error is not None:
            raise cache_record.error

    def _worker(self) -> None:
        try:
            while True:
                first = self._q.get()
                if first is None:
                    self._q.task_done()
                    break
                batch = [first]
                deadline = time.monotonic() + self._max_batch_delay
                while len(batch) < self._max_batch_size:
                    now = time.monotonic()
                    timeout = deadline - time.monotonic()
                    if timeout <= 0:
                        break
                    try:
                        # why is it blocking here?
                        item = self._q.get(timeout=timeout)
                    except queue.Empty:
                       break
                    if item is None:
                        self._q.task_done()
                        self._commit_batch(batch)
                        return
                    batch.append(item)

                self._commit_batch(batch)
        finally:
            self._walfile.close()


    def _commit_batch(self, batch: list[CacheRecord]):
        error = None
        try:
            for item in batch:
                header, payload = self._encode(item)
                self._walfile.buffer.write(header)
                self._walfile.buffer.write(payload)
            self._walfile.flush()
            os.fsync(self._walfile.fileno()) # this is very expensive on every put
        except BaseException as exc:
            error = exc
        finally:
            with self._lock:
                for item in batch:
                    item.error = error
                    self._q.task_done()
                    if error:
                        item.done.set()
                        continue
                    match item.op:
                        case 'put':
                            self._store[item.key] = item.value
                            item.done.set()
                        case 'del':
                            self._store.pop(item.key, None)
                            item.done.set()



def main():
    cache = DCache()
    try:
        while True:
            command = input('cache>')
            if command.startswith('get'):
                _, key = command.split()
                value = cache.get(key)
                print('value: ', value)
            elif command.startswith('set'):
                _, key, value = command.split()
                cache.put(key, value)
                print('+ok')
            elif command.startswith('del'):
                _, key = command.split()
                cache.delete(key)
                print('+ok')
    except BaseException:
        print('exciting')
    finally:
        cache.close()


if __name__ == '__main__':
    main()
