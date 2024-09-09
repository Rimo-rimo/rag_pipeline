import os
import time
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer

class Target:
    watchDir = "/home/livin/rag_pipeline/data"  # 감시하려는 디렉토리

    def __init__(self):
        self.observer = Observer()  # observer 객체 생성

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.file_hashes = {}  # 파일의 해시값을 저장할 딕셔너리
        self.debounce_timers = {}  # 파일별로 이벤트 처리 지연 타이머 저장

    def calculate_hash(self, file_path):
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except FileNotFoundError:
            return None
        return hash_md5.hexdigest()

    def handle_modified(self, file_path):
        """Debounced 함수: 실제 파일 변경 내용을 처리"""
        new_hash = self.calculate_hash(file_path)
        old_hash = self.file_hashes.get(file_path)

        if new_hash and new_hash != old_hash:
            print(f"파일 수정됨: {file_path}")
            self.file_hashes[file_path] = new_hash
        else:
            print(f"파일 수정 이벤트 발생했으나 내용 변경 없음: {file_path}")

        # 처리 후 타이머 제거
        self.debounce_timers.pop(file_path, None)

    def on_modified(self, event):
        if not event.is_directory:
            # 기존 타이머가 있으면 취소하고 새로 설정
            if event.src_path in self.debounce_timers:
                self.debounce_timers[event.src_path].cancel()

            # 0.5초 후에 수정 이벤트를 처리하도록 타이머 설정
            timer = Timer(0.5, self.handle_modified, args=[event.src_path])
            self.debounce_timers[event.src_path] = timer
            timer.start()

    def on_created(self, event):
        if not event.is_directory:
            print(f"파일 생성됨: {event.src_path}")
            self.file_hashes[event.src_path] = self.calculate_hash(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"파일 삭제됨: {event.src_path}")
            self.file_hashes.pop(event.src_path, None)

    def on_moved(self, event):
        if not event.is_directory:
            print(f"파일 path 변경: {event.src_path} -> {event.dest_path}")
            self.file_hashes[event.dest_path] = self.file_hashes.pop(event.src_path, None)

if __name__ == "__main__":  # 본 파일에서 실행될 때만 실행되도록 함
    print("run watchdog")
    w = Target()
    w.run()

