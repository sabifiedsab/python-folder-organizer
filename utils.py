import os
from pathlib import Path

def list_directories(main_dir, subdir: str = "") -> list[str]:
    """Lists all directories within the main directory."""
    directories = []
    for entry in os.listdir(os.path.join(main_dir, subdir)):
        directories.append(Path(os.path.join(main_dir, subdir, entry)))
    return directories
