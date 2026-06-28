from pathlib import Path


BASE_DIR = Path(__file__).parent


def total_salary(path):
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                _, salary = line.split(",")
                total += int(salary)
                count += 1

        if count == 0:
            return 0, 0

        return total, total / count

    except FileNotFoundError:
        print(f"File not found: {path}")
        return 0, 0
    except ValueError:
        print("Invalid file format.")
        return 0, 0
    except Exception as error:
        print(f"An error occurred: {error}")
        return 0, 0


if __name__ == "__main__":
    salary_path = BASE_DIR / "salary_file.txt"
    total, average = total_salary(salary_path)
    print(f"Total salary: {total}")
    print(f"Average salary: {average}")
