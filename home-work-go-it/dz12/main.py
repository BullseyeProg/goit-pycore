from collections import UserDict
from datetime import datetime, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        return value.isdigit() and len(value) == 10


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)

        if phone_obj is None:
            raise ValueError("Phone not found.")

        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)

        if phone_obj is None:
            raise ValueError("Old phone not found.")

        phone_obj.value = Phone(new_phone).value

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj

        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(str(phone) for phone in self.phones)

        if self.birthday:
            return (
                f"Contact name: {self.name.value}, "
                f"phones: {phones}, "
                f"birthday: {self.birthday.value}"
            )

        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name not in self.data:
            raise KeyError("Contact not found.")

        del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday_date = datetime.strptime(
                record.birthday.value,
                "%d.%m.%Y"
            ).date()

            birthday_this_year = birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(
                    year=today.year + 1
                )

            days_difference = (birthday_this_year - today).days

            if 0 <= days_difference <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)

                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError as error:
            return str(error)

        except KeyError as error:
            return str(error)

        except IndexError:
            return "Not enough arguments."

    return inner


def parse_input(user_input):
    parts = user_input.strip().split()

    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]

    return command, args


@input_error
def add_contact(args, book):
    name = args[0]
    phone = args[1]

    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

    record.add_phone(phone)
    return "Phone added to existing contact."


@input_error
def change_contact(args, book):
    name = args[0]
    old_phone = args[1]
    new_phone = args[2]

    record = book.find(name)

    if record is None:
        raise ValueError("Contact not found.")

    record.edit_phone(old_phone, new_phone)

    return "Contact updated."


@input_error
def show_phone(args, book):
    name = args[0]

    record = book.find(name)

    if record is None:
        raise ValueError("Contact not found.")

    if not record.phones:
        return "This contact has no phones."

    return "; ".join(str(phone) for phone in record.phones)


def show_all(book):
    if not book.data:
        return "Address book is empty."

    result = []

    for record in book.data.values():
        result.append(str(record))

    return "\n".join(result)


@input_error
def add_birthday(args, book):
    name = args[0]
    birthday = args[1]

    record = book.find(name)

    if record is None:
        raise ValueError("Contact not found.")

    record.add_birthday(birthday)

    return "Birthday added."


@input_error
def show_birthday(args, book):
    name = args[0]

    record = book.find(name)

    if record is None:
        raise ValueError("Contact not found.")

    if record.birthday is None:
        return "Birthday not found."

    return record.birthday.value


def birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays()

    if not upcoming_birthdays:
        return "No upcoming birthdays."

    result = []

    for item in upcoming_birthdays:
        result.append(
            f"{item['name']}: {item['congratulation_date']}"
        )

    return "\n".join(result)


@input_error
def delete_contact(args, book):
    name = args[0]

    book.delete(name)

    return "Contact deleted."


@input_error
def remove_phone(args, book):
    name = args[0]
    phone = args[1]

    record = book.find(name)

    if record is None:
        raise ValueError("Contact not found.")

    record.remove_phone(phone)

    return "Phone removed."


def main():
    book = load_data()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Address book saved.")
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        elif command == "delete":
            print(delete_contact(args, book))

        elif command == "remove-phone":
            print(remove_phone(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()