import sys
from pathlib import Path


def print_directory_tree(path, prefix=""):
    path = Path(path)

    if not path.exists():
        print(f"Path does not exist: {path}")
        return

    if not path.is_dir():
        print(f"Not a directory: {path}")
        return

    items = sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))

    for index, item in enumerate(items):
        is_last = index == len(items) - 1
        connector = "`-- " if is_last else "|-- "

        if item.is_dir():
            print(f"{prefix}{connector}{item.name}/")
            next_prefix = prefix + ("    " if is_last else "|   ")
            print_directory_tree(item, next_prefix)
        else:
            print(f"{prefix}{connector}{item.name}")


def run_tree_mode(directory_path):
    directory = Path(directory_path)

    if not directory.exists():
        print(f"Path does not exist: {directory_path}")
        return

    if not directory.is_dir():
        print(f"Not a directory: {directory_path}")
        return

    print(f"{directory.name}/")
    print_directory_tree(directory)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_tree_mode(sys.argv[1])
    else:
        print("Usage: python 3.py <directory_path>")
