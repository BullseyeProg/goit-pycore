from pathlib import Path
import sys


# Папка, где лежит сам файл hw03.py
BASE_DIR = Path(__file__).parent


# ============================================================
# Завдання 1
# ============================================================

def total_salary(path):
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                name, salary = line.split(",")
                total += int(salary)
                count += 1

        if count == 0:
            return 0, 0

        average = total / count
        return total, average

    except FileNotFoundError:
        print(f"Файл не знайдено: {path}")
        return 0, 0

    except ValueError:
        print("Помилка у форматі файлу.")
        return 0, 0

    except Exception as error:
        print(f"Сталася помилка: {error}")
        return 0, 0


# ============================================================
# Завдання 2
# ============================================================

def get_cats_info(path):
    cats = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                cat_id, name, age = line.split(",")

                cat = {
                    "id": cat_id,
                    "name": name,
                    "age": age
                }

                cats.append(cat)

        return cats

    except FileNotFoundError:
        print(f"Файл не знайдено: {path}")
        return []

    except ValueError:
        print("Помилка у форматі файлу.")
        return []

    except Exception as error:
        print(f"Сталася помилка: {error}")
        return []


# ============================================================
# Завдання 3 python ".\dz6\hw03.py" "C:\Users\Dima Kozyrev\PyCharmMiscProject\dz4\dz6"
# ============================================================

def print_directory_tree(path, prefix=""):
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)
    except ImportError:
        print("Бібліотека colorama не встановлена.")
        print("Встановіть її командою:")
        print("pip install colorama")
        return

    path = Path(path)

    if not path.exists():
        print(f"Помилка: шлях не існує: {path}")
        return

    if not path.is_dir():
        print(f"Помилка: це не директорія: {path}")
        return

    items = list(path.iterdir())

    for index, item in enumerate(items):
        is_last = index == len(items) - 1

        if is_last:
            connector = "┗ "
        else:
            connector = "┣ "

        if item.is_dir():
            print(prefix + connector + Fore.BLUE + "📂 " + item.name + Style.RESET_ALL)

            if is_last:
                new_prefix = prefix + "  "
            else:
                new_prefix = prefix + "┃ "

            print_directory_tree(item, new_prefix)

        else:
            print(prefix + connector + Fore.GREEN + "📜 " + item.name + Style.RESET_ALL)


def run_tree_mode(directory_path):
    directory = Path(directory_path)

    if not directory.exists():
        print(f"Помилка: шлях не існує: {directory_path}")
        return

    if not directory.is_dir():
        print(f"Помилка: це не директорія: {directory_path}")
        return

    print("📦" + directory.name)
    print_directory_tree(directory)


# ============================================================
# Завдання 4
# ============================================================

def parse_input(user_input):
    parts = user_input.strip().split()

    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]

    return command, args


def add_contact(args, contacts):
    if len(args) != 2:
        return "Invalid command."

    name, phone = args
    contacts[name] = phone

    return "Contact added."


def change_contact(args, contacts):
    if len(args) != 2:
        return "Invalid command."

    name, phone = args

    if name not in contacts:
        return "Contact not found."

    contacts[name] = phone

    return "Contact updated."


def show_phone(args, contacts):
    if len(args) != 1:
        return "Invalid command."

    name = args[0]

    if name not in contacts:
        return "Contact not found."

    return contacts[name]


def show_all(contacts):
    if not contacts:
        return "No contacts found."

    result = []

    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")

    return "\n".join(result)


def main():
    contacts = {}

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "all":
            print(show_all(contacts))

        else:
            print("Invalid command.")


# ============================================================
# Запуск
# ============================================================

if __name__ == "__main__":

    # Якщо запустити:
    # python hw03.py bot
    # запуститься бот із завдання 4
    if len(sys.argv) > 1 and sys.argv[1].lower() == "bot":
        main()

    # Якщо запустити:
    # python hw03.py C:\Users\Dima Kozyrev\PyCharmMiscProject\dz4\dz6
    # запуститься завдання 3
    elif len(sys.argv) > 1:
        run_tree_mode(sys.argv[1])

    # Якщо просто запустити:
    # python hw03.py
    # перевіряться завдання 1 і 2
    else:
        salary_path = BASE_DIR / "salary_file.txt"
        cats_path = BASE_DIR / "cats_file.txt"

        print("=== Завдання 1 ===")
        total, average = total_salary(salary_path)
        print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")

        print()

        print("=== Завдання 2 ===")
        cats_info = get_cats_info(cats_path)
        print(cats_info)

        print()
        print("Щоб запустити бота:")
        print("python hw03.py bot")

        print()
        print("Щоб вивести дерево директорії:")
        print("python hw03.py шлях_до_директорії")