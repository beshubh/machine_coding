import os
import threading
import queue
import zlib

import time

from pathlib import Path
from dataclasses import dataclass

# Async logs, no guranee that log() will persist the data
class Log:

    def __init__(
        self,
        path: str | Path = "log.log",
        *,
        flush_interval: float = 1.0
    ):
        self._q = queue.Queue()
        self._path = path
        self._flush_interval = flush_interval
        self._file = open(self._path, mode='a', encoding='utf-8')
        self._closed = False


        self._thread = threading.Thread(daemon=True, target=self._worker)
        self._thread.start()


    def log(self, message: str) -> None:
        if self._closed:
            raise RuntimeError('cannot write to closed log')
        self._q.put(message)

    def close(self) -> None:
        if self._closed:
            return

        self._closed = True
        # send a sentinel to the worker to finish
        self._q.put(None)
        # wait till worker thread finishes
        self._thread.join()

    def _worker(self):
        last_flush = time.monotonic()
        while True:
            msg = self._q.get()
            try:
                if msg is None:
                    break
                self._file.write(msg + '\n')
                now = time.monotonic()
                if now - last_flush >= self._flush_interval:
                    self._file.flush()
                    last_flush = now
            finally:
                self._q.task_done()
        while True:
            try:
                msg = self._q.get_nowait()
            except queue.Empty:
                break

            try:
                if msg is None:
                    self._file.write(msg + '\n')
            finally:
                self._q.task_done()

        self._file.flush()

    def __enter__(self) -> "Log":
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.close()






def write_some_logs(log: Log):
    log.log("")
    log.log("hello t2")
    log.log("hello 5")
    log.log("helo 6")
    log.log("hello 8")
    log.log("hello 9")


def main():
    with Log("log.log") as log:
        try:
            print('press ctrl + c to stop')
            write_some_logs(log)

            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('shutting down')


if __name__ == '__main__':
    main()

@dataclass
class LogRecord:
    message: str
    done: threading.Event
    error: BaseException | None = None


class DurableBatchingLog:

    def __init__(
        self,
        path: str | Path,
        *,
        max_batch_size: int = 128,
        max_batch_delay: float = 0.005,
    ):
        self._path = Path(path)
        self._q = queue.Queue[LogRecord | None]()
        self._closed = False
        self._close_lock = threading.Lock()

        self._max_batch_size = max_batch_size
        self._max_batch_delay = max_batch_delay

        self._file = open(self._path, mode='a', encoding='utf-8')
        self._thread = threading.Thread(target=self._worker)
        self._thread.start()


    def recover(self):
        good_offset = 0
        with open(self._path, 'rb+') as f:
            while True:
                header = f.readline()
                if not header:
                    break
                try:
                    length_s, checksum_s = header.decode().strip().split()
                    length = int(length_s)
                    expected_checksum = int(checksum_s)
                except (ValueError, TypeError):
                    break
                payload = f.read(length)
                if len(payload) != length:
                    break

                newline = f.read(1)
                if newline != b"\n":
                    break

                actual_checksum = zlib.crc32(payload)
                if actual_checksum != expected_checksum:
                    break
                good_offset = f.tell()
        f.truncate(good_offset)


    def log(self, message: str) -> None:
        record = LogRecord(
            message=message,
            done=threading.Event(),
        )
        with self._close_lock:
            if self._closed:
                raise RuntimeError('Log is closed')
            self._q.put(record)

        # Synchronous durability
        record.done.wait()
        if record.error is not None:
            raise record.error


    def close(self) -> None:
        with self._close_lock:
            if self._closed:
                return

            self._closed = True
            self._q.put(None) # sentinel to indicate end

        self._thread.join()

    def _worker(self) -> None:
        try:
            while True:
                first = self._q.get()
                if first is None:
                    self._q.task_done()
                    break

                batch: list[LogRecord] = [first]
                deadline = time.monotonic() + self._max_batch_delay

                while len(batch) < self._max_batch_size:
                    timeout = deadline - time.monotonic()
                    if timeout <= 0:
                        break
                    try:
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
            self._file.close()

    def _commit_batch(self, batch: list[LogRecord]) -> None:
        error: BaseException | None = None

        try:
            for record in batch:
                payload = record.message.encode('utf-8')
                checksum = zlib.crc32(payload)
                header = f"{len(payload)} {checksum}\n".encode()
                self._file.buffer.write(header)
                self._file.buffer.write(payload)
                self._file.buffer.write(b'\n')
                # what if we crash here?

            self._file.flush()
            os.fsync(self._file.fileno())
        except BaseException as exc:
            error = exc
        finally:
            for record in batch:
                record.error = error
                record.done.set()
                self._q.task_done()

    def __enter__(self) -> 'DurableBatchingLog':
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

