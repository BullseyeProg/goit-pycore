import re


def normalize_phone(phone_number: str) -> str:


    # Видаляємо пробіли по краях
    phone_number = phone_number.strip()

    # Залишаємо тільки цифри та +
    phone_number = re.sub(r"[^\d+]", "", phone_number)

    # Якщо номер починається з +
    if phone_number.startswith("+"):
        return phone_number

    # Якщо починається з 380 (але без +)
    if phone_number.startswith("380"):
        return "+" + phone_number

    # Якщо починається з 0 (локальний номер)
    if phone_number.startswith("0"):
        return "+38" + phone_number

    # На випадок інших варіантів
    return "+38" + phone_number
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
