from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Клас для зберігання імені контакту.
    Ім'я є обов'язковим полем.
    """

    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")

        super().__init__(value)


class Phone(Field):
    """
    Клас для зберігання номера телефону.
    Номер телефону має складатися рівно з 10 цифр.
    """

    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits")

        super().__init__(value)

    @staticmethod
    def is_valid_phone(value):
        return value.isdigit() and len(value) == 10


class Record:
    """
    Клас для зберігання одного контакту.
    Містить ім'я контакту та список телефонів.
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """
        Додає телефон до контакту.
        """

        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        """
        Видаляє телефон з контакту.
        """

        phone_to_remove = self.find_phone(phone)

        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone, new_phone):
        """
        Редагує існуючий телефон.
        """

        phone_to_edit = self.find_phone(old_phone)

        if phone_to_edit is None:
            raise ValueError("Phone not found")

        new_phone_obj = Phone(new_phone)

        phone_to_edit.value = new_phone_obj.value

    def find_phone(self, phone):
        """
        Шукає телефон у списку телефонів контакту.
        Повертає об'єкт Phone або None.
        """

        for item in self.phones:
            if item.value == phone:
                return item

        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(phone.value for phone in self.phones)}"


class AddressBook(UserDict):
    """
    Клас для зберігання записів контактів.
    Наслідується від UserDict.
    """

    def add_record(self, record):
        """
        Додає запис до адресної книги.
        Ключем є ім'я контакту.
        """

        self.data[record.name.value] = record

    def find(self, name):
        """
        Шукає запис за ім'ям.
        Повертає Record або None.
        """

        return self.data.get(name)

    def delete(self, name):
        """
        Видаляє запис за ім'ям.
        """

        if name in self.data:
            del self.data[name]


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")

    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print("=== Всі контакти ===")

    for name, record in book.data.items():
        print(record)

    print()

    # Знаходження та редагування телефону для John
    john = book.find("John")

    if john:
        john.edit_phone("1234567890", "1112223333")
        print("=== Після редагування John ===")
        print(john)

    print()

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")

    print("=== Знайдений телефон ===")
    print(f"{john.name}: {found_phone}")

    print()

    # Видалення запису Jane
    book.delete("Jane")

    print("=== Після видалення Jane ===")

    for name, record in book.data.items():
        print(record)