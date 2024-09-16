import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

downloads_folder = os.path.expanduser("~/Downloads")

file_types = {
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.pptx', '.ppt', '.xlsx', '.xls'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'],
    'Music': ['.mp3', '.wav', '.aac', '.flac'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z']
}

def create_folders():
    for category in file_types.keys():
        category_path = os.path.join(downloads_folder, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
    other_path = os.path.join(downloads_folder, 'Others')
    if not os.path.exists(other_path):
        os.mkdir(other_path)

def move_files(filename):
    file_path = os.path.join(downloads_folder, filename)

    if os.path.isfile(file_path):
        moved = False
        file_ext = os.path.splitext(filename)[1].lower()

        for category, extensions in file_types.items():
            if file_ext in extensions:
                shutil.move(file_path, os.path.join(downloads_folder, category, filename))
                print(f"Moved {filename} to {category}")
                moved = True
                break

        if not moved:
            shutil.move(file_path, os.path.join(downloads_folder, 'Others', filename))
            print(f"Moved {filename} to Others")

class DownloadsHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(downloads_folder):
            move_files(filename)

if __name__ == "__main__":
    create_folders()

    event_handler = DownloadsHandler()
    observer = Observer()
    observer.schedule(event_handler, downloads_folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
