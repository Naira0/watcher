from os import path, mkdir
from sys import argv
from logging import basicConfig, INFO
from time import sleep
from shutil import copy
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler

current_path = path.dirname(path.realpath(__file__))

if not path.exists(current_path + '/backups'):
    mkdir(current_path + '/backups')

del argv[0]
observer_path = str(' '.join(argv)) if len(argv) > 0 else input("Enter path to folder: ")

print("Observing folder!")

def handle_copy(src):

    folder_date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    copy_dir = f'{current_path}\\backups\\{folder_date}'

    if not path.exists(copy_dir):
        mkdir(copy_dir)
    try:
        copy(src, copy_dir)
    except (PermissionError, FileNotFoundError) as error:
        print("Error backing up files")
        print(f"Error code: {error}")

def on_created(event):
    handle_copy(event.src_path)

def on_modify(event):
    handle_copy(event.src_path)

if __name__ == "__main__":
    basicConfig(level=INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    log_handler = LoggingEventHandler()
    event_handler = PatternMatchingEventHandler('*', '', False, True)

    event_handler.on_created = on_created
    event_handler.on_modified = on_modify

    observer = Observer()
    
    observer.schedule(log_handler, observer_path, recursive=False)
    observer.schedule(event_handler, observer_path, recursive=True)

    observer.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
