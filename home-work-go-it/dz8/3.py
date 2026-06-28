from collections import defaultdict
import sys


def parse_log_line(line: str) -> dict:
    parts = line.strip().split(" ", 3)

    if len(parts) != 4:
        raise ValueError(f"Неправильний формат рядка логу: {line}")

    date, time, level, message = parts
    return {
        "date": date,
        "time": time,
        "level": level.upper(),
        "message": message,
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


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1].lower() == "logs":
        log_file_path = sys.argv[2]
        log_level = sys.argv[3] if len(sys.argv) > 3 else None
        run_logs_mode(log_file_path, log_level)
    else:
        print("Usage: python 3.py logs <logfile> [level]")
