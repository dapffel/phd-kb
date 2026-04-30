import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from agents.config import settings
from agents.supervisor.graph import Supervisor


class PDFHandler(FileSystemEventHandler):
    def __init__(self, supervisor: Supervisor):
        self.supervisor = supervisor

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".pdf"):
            filename = event.src_path.split("/")[-1]
            print(f"\n[watcher] New PDF detected: {filename}")
            output = self.supervisor.run("ingest", filename)
            print(output)


def watch():
    supervisor = Supervisor()
    handler = PDFHandler(supervisor)
    observer = Observer()
    observer.schedule(handler, str(settings.papers_dir), recursive=False)
    observer.start()
    print(f"Watching {settings.papers_dir} for new PDFs... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
