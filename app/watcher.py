# ==========================================
# 👀 SQUIRREL FILE WATCHER
# ==========================================

from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ==========================================
# 🐿️ FILE EVENT HANDLER
# ==========================================

class SquirrelHandler(FileSystemEventHandler):

    def __init__(
        self,
        analyze_function
    ):

        super().__init__()

        self.analyze_function = (
            analyze_function
        )

    # ======================================
    # 📁 NEW FILE DETECTED
    # ======================================

    def on_created(
        self,
        event
    ):

        # Ignore folders
        if event.is_directory:

            return

        file_path = Path(
            event.src_path
        )

        print()
        print(
            "🐿️ CHIP DETECTED SOMETHING!"
        )

        print(
            f"📁 File: {file_path.name}"
        )

        # Send the file to main.py
        self.analyze_function(
            file_path
        )

    # ======================================
    # 📦 FILE MOVED INTO PLAYGROUND
    # ======================================

    def on_moved(
        self,
        event
    ):

        # Ignore folders
        if event.is_directory:

            return

        file_path = Path(
            event.dest_path
        )

        print()
        print(
            "🐿️ CHIP NOTICED A FILE ARRIVING!"
        )

        print(
            f"📁 File: {file_path.name}"
        )

        self.analyze_function(
            file_path
        )


# ==========================================
# 👀 START WATCHING
# ==========================================

def start_watching(
    playground,
    analyze_function
):

    playground = Path(
        playground
    )

    # Make absolutely sure the directory exists
    playground.mkdir(
        parents=True,
        exist_ok=True
    )

    event_handler = SquirrelHandler(
        analyze_function
    )

    observer = Observer()

    observer.schedule(
        event_handler,
        str(playground),
        recursive=False
    )

    observer.start()

    print()
    print(
        "👀 CHIP IS WATCHING:"
    )

    print(
        f"📂 {playground}"
    )

    return observer