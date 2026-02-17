from datetime import datetime, timedelta


def get_upcoming_birthdays(users: list) -> list:
    """
    Повертає список користувачів, у яких день народження
    протягом наступних 7 днів (включно з сьогоднішнім).
    Якщо дата припадає на вихідний — переносить на понеділок.
    """

    today = datetime.today().date()
    upcoming_birthdays = []

    for user in users:
        # Перетворюємо рядок у дату
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()

        # День народження у поточному році
        birthday_this_year = birthday.replace(year=today.year)

        # Якщо вже минув — беремо наступний рік
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        # Різниця в днях
        delta_days = (birthday_this_year - today).days

        # Якщо в межах 7 днів
        if 0 <= delta_days <= 7:

            congratulation_date = birthday_this_year

            # Якщо субота
            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)

            # Якщо неділя
            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })

    return upcoming_birthdays
