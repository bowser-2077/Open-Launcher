# services/downloader.py
import requests
from PySide6.QtCore import QThread, Signal

class DownloadThread(QThread):
    progress = Signal(int)     #pgress bar
    finished = Signal(str)     # game path
    error = Signal(str)        # err

    def __init__(self, url, dest):
        super().__init__()
        self.url = url
        self.dest = dest

    def run(self):
        try:
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0))
                downloaded = 0

                with open(self.dest, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total > 0:
                                percent = int(downloaded * 100 / total)
                                self.progress.emit(percent)

            self.finished.emit(self.dest)

        except Exception as e:
            self.error.emit(str(e))

