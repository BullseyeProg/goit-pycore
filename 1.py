import datetime

def get_days_from_today():
    today_date = datetime.date.today()
    print(today_date)
    try:
        date_str = input ("input date (YYYY-MM-DD): ")
        print(date_str)
        parts = date_str.split('-')
        date_str = datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
        difference = today_date - date_str
        print(difference.days)
    except (ValueError, IndexError):
        print("Неправильный ввод! Используйте формат YYYY-MM-DD и корректные числа.")
get_days_from_today()