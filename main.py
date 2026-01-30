import threading
from dependencies import gather_dependencies
from wxUI import start_ui

if __name__ == "__main__":
    gather_dependencies()
    start_ui()

