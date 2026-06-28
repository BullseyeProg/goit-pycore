from functools import wraps


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

    return parts[0].lower(), parts[1:]


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

    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


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


if __name__ == "__main__":
    bot_main()
