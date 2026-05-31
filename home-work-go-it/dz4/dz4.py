from datetime import datetime, date, timedelta
import random
import re


# ============================================================
# Завдання 1
# ============================================================

def get_days_from_today(date_str: str) -> int | None:
    """
    Приймає дату у форматі 'YYYY-MM-DD'
    і повертає різницю між сьогоднішньою датою та заданою датою в днях.
    """

    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = date.today()

        difference = today - input_date

        return difference.days

    except ValueError:
        print("Неправильний формат дати. Використовуйте формат YYYY-MM-DD.")
        return None


# Приклад перевірки завдання 1
result = get_days_from_today("2021-10-09")
print("Різниця у днях:", result)


# ============================================================
# Завдання 2
# ============================================================

def get_numbers_ticket(min: int, max: int, quantity: int) -> list:
    """
    Повертає відсортований список унікальних випадкових чисел.

    min — мінімальне можливе число, не менше 1
    max — максимальне можливе число, не більше 1000
    quantity — кількість чисел, які потрібно вибрати
    """

    if min < 1:
        return []

    if max > 1000:
        return []

    if min > max:
        return []

    if quantity < 1:
        return []

    if quantity > max - min + 1:
        return []

    numbers = random.sample(range(min, max + 1), quantity)

    return sorted(numbers)


# Приклад перевірки завдання 2
lottery_numbers = get_numbers_ticket(1, 60, 10)
print("Ваші лотерейні числа:", lottery_numbers)


# ============================================================
# Завдання 3
# ============================================================

def normalize_phone(phone_number: str) -> str:
    """
    Нормалізує номер телефону до формату +380...
    """

    phone_number = phone_number.strip()

    phone_number = re.sub(r"[^\d+]", "", phone_number)

    if phone_number.startswith("+"):
        return phone_number

    if phone_number.startswith("380"):
        return "+" + phone_number

    return "+38" + phone_number


# Приклад перевірки завдання 3
raw_numbers = [
    "067\t123 4567",
    "(095) 234-5678\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Нормалізовані номери:", sanitized_numbers)


# ============================================================
# Завдання 4
# ============================================================

def get_upcoming_birthdays(users: list) -> list:
    """
    Повертає список користувачів, яких потрібно привітати
    протягом наступних 7 днів.

    Якщо день народження припадає на суботу або неділю,
    дата привітання переноситься на понеділок.
    """

    today = date.today()
    upcoming_birthdays = []

    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()

        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        days_difference = (birthday_this_year - today).days

        if 0 <= days_difference <= 7:
            congratulation_date = birthday_this_year

            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)

            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })

    return upcoming_birthdays


# Приклад перевірки завдання 4
users = [
    {"name": "John Doe", "birthday": "1985.06.03"},
    {"name": "Jane Smith", "birthday": "1990.06.07"},
    {"name": "Bob Johnson", "birthday": "1992.12.20"},
]

upcoming = get_upcoming_birthdays(users)
print("Найближчі дні народження:", upcoming)