import re
import sys
from collections import defaultdict
from functools import wraps
from typing import Callable, Generator


# ============================================================
# Завдання 1
# caching_fibonacci
# ============================================================

def caching_fibonacci():


    cache = {}

    def fibonacci(n: int) -> int:


        if n <= 0:
            return 0

        if n == 1:
            return 1

        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)

        return cache[n]

    return fibonacci


# ============================================================
# Завдання 2
# generator_numbers та sum_profit
# ============================================================

def generator_numbers(text: str) -> Generator[float, None, None]:


    pattern = r"(?<!\S)\d+(?:\.\d+)?(?!\S)"

    for number in re.findall(pattern, text):
        yield float(number)


def sum_profit(text: str, func: Callable) -> float:


    return sum(func(text))


# ============================================================
# Завдання 3
# Аналіз лог-файлу
# ============================================================

def parse_log_line(line: str) -> dict:


    parts = line.strip().split(" ", 3)

    if len(parts) != 4:
        raise ValueError(f"Неправильний формат рядка логу: {line}")

    date, time, level, message = parts

    return {
        "date": date,
        "time": time,
        "level": level.upper(),
        "message": message
    }


def load_logs(file_path: str) -> list:

    logs = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    logs.append(parse_log_line(line))

    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")

    except ValueError as error:
        print(error)

    except Exception as error:
        print(f"Сталася помилка при читанні файлу: {error}")

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:


    level = level.upper()

    return list(filter(lambda log: log["level"] == level, logs))


def count_logs_by_level(logs: list) -> dict:


    counts = defaultdict(int)

    for log in logs:
        counts[log["level"]] += 1

    return dict(counts)


def display_log_counts(counts: dict) -> None:


    print("Рівень логування | Кількість")
    print("-----------------|----------")

    for level in ["INFO", "DEBUG", "ERROR", "WARNING"]:
        print(f"{level:<16} | {counts.get(level, 0)}")


def display_logs_details(logs: list, level: str) -> None:


    filtered_logs = filter_logs_by_level(logs, level)

    print()
    print(f"Деталі логів для рівня '{level.upper()}':")

    if not filtered_logs:
        print("Записів не знайдено.")
        return

    for log in filtered_logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def run_logs_mode(file_path: str, level: str | None = None) -> None:


    logs = load_logs(file_path)

    if not logs:
        return

    counts = count_logs_by_level(logs)

    display_log_counts(counts)

    if level:
        display_logs_details(logs, level)


# ============================================================
# Завдання 4
# Бот з декоратором input_error
# ============================================================

def input_error(func):


    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError:
            return "Give me name and phone please."

        except KeyError:
            return "Enter user name."

        except IndexError:
            return "Enter the argument for the command."

    return inner


def parse_input(user_input: str) -> tuple[str, list]:


    parts = user_input.strip().split()

    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]

    return command, args


@input_error
def add_contact(args: list, contacts: dict) -> str:


    if len(args) != 2:
        raise IndexError

    name, phone = args
    name = name.lower()

    contacts[name] = phone

    return "Contact added."


@input_error
def change_contact(args: list, contacts: dict) -> str:


    if len(args) != 2:
        raise IndexError

    name, phone = args
    name = name.lower()

    if name not in contacts:
        raise KeyError

    contacts[name] = phone

    return "Contact updated."


@input_error
def show_phone(args: list, contacts: dict) -> str:


    if len(args) != 1:
        raise IndexError

    name = args[0].lower()

    if name not in contacts:
        raise KeyError

    return contacts[name]


@input_error
def show_all(contacts: dict) -> str:


    if not contacts:
        return "No contacts found."

    result = []

    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")

    return "\n".join(result)


def bot_main() -> None:


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
# Демонстрація завдань 1 та 2
# ============================================================

def demo_task_1_and_2() -> None:


    print("=== Завдання 1 ===")

    fib = caching_fibonacci()

    print(fib(10))
    print(fib(15))

    print()
    print("=== Завдання 2 ===")

    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими "
        "надходженнями 27.45 і 324.00 доларів."
    )

    total_income = sum_profit(text, generator_numbers)

    print(f"Загальний дохід: {total_income}")


# ============================================================
# Запуск програми
# ============================================================

if __name__ == "__main__":

    # Запуск бота:
    # python main.py bot

    if len(sys.argv) > 1 and sys.argv[1].lower() == "bot":
        bot_main()

    # Запуск аналізатора логів:
    # python main.py logs logfile.log
    # python main.py logs logfile.log error

    elif len(sys.argv) > 2 and sys.argv[1].lower() == "logs":
        log_file_path = sys.argv[2]

        if len(sys.argv) > 3:
            log_level = sys.argv[3]
        else:
            log_level = None

        run_logs_mode(log_file_path, log_level)

    # Якщо запустити просто:
    # python main.py
    # перевіряться завдання 1 і 2

    else:
        demo_task_1_and_2()