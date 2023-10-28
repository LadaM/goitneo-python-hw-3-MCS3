import json
import os

from pathlib import Path
from constants import COMMANDS, CONTACTS_FILE
from exceptions import ValueNotFound, InvalidCommand, DuplicateEntry


def main():
    print("Welcome to the assistant bot!")
    while True:
        command = input("Enter a command: ").strip().lower()
        try:
            if command == "hello":
                print("How can I help you?")
            elif command.startswith("add"):
                try:
                    _, name, phone = command.split(' ')
                    msg = add_contact(name, phone)
                    print(msg)
                except ValueError:
                    raise InvalidCommand(COMMANDS.get('add'))
            elif command.startswith("change"):
                try:
                    _, name, phone = command.split(' ')
                    msg = update_contact(name, phone)
                    print(msg)
                except ValueError:
                    raise InvalidCommand(COMMANDS.get('update'))
            elif command.startswith("phone"):
                try:
                    _, name = command.split(' ')
                    phone = get_phone(name)
                    print(phone)
                except ValueError:
                    raise InvalidCommand(COMMANDS.get('phone'))
            elif command.startswith("all"):
                msg = show_all_contacts()
                print(msg)
            elif command in ["close", "exit"]:
                print("Goodbye!")
                break
            else:
                raise InvalidCommand
        except InvalidCommand as e:
            print(f"Expecting command in form {e.command}" if e.command else
                  ("Ivalid command recieved. Accepted commands are:\n{}"
                   .format('\n'.join(['- ' + s for s in COMMANDS.values()]))))
            continue


file_path = Path.cwd().joinpath(CONTACTS_FILE)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DuplicateEntry as error:
            return f"We alreay have a contact with name {error.name}"
        except ValueNotFound as error:
            return f"No contact for name {error.name} found"
        except FileNotFoundError:
            # if the file is empty there are no contacts to show
            return "We haven't stored any contacts yet"

    return inner


@input_error
def add_contact(name: str, phone: str):
    try:
        contacts = get_contacts()
    except FileNotFoundError:
        # if there is no file yet or it is empty, we just create one and add contact
        contacts = []

    for c in contacts:
        # if we already have a name in our contact list, we don't add it again
        n = c.get("name")
        if n == name:
            raise DuplicateEntry(name)

    contact = {"name": name, "phone": phone}
    contacts.append(contact)
    with open(file_path, 'w') as json_file:
        json.dump(contacts, json_file, indent=4)

    return "Contact added"


@input_error
def update_contact(name, phone):
    try:
        contacts = get_contacts()
        updated = False
        for c in contacts:
            if c.get("name") == name:
                c["phone"] = phone
                updated = True
        with open(file_path, 'w') as json_file:
            json.dump(contacts, json_file, indent=4)
        if not updated:
            raise ValueNotFound(name)
    except FileNotFoundError:
        # if the file is empty, our name isn't in the file
        raise ValueNotFound(name)

    return "Contact updated"


@input_error
def get_phone(name):
    try:
        contacts = get_contacts()
        for c in contacts:
            if c.get("name") == name:
                return c["phone"]
        # if there was no match, then there is no such contact stored
        raise ValueNotFound(name)
    except FileNotFoundError:
        # if the file is empty, our name isn't in the file
        raise ValueNotFound(name)


@input_error
def show_all_contacts():
    contacts = get_contacts()
    return '\n'.join(map(lambda contact: f"{contact.get('name'):<10}{contact.get('phone'):<10}", contacts))


def get_contacts():
    file_not_empty = os.path.isfile(
        file_path) and os.path.getsize(file_path) > 0
    if file_not_empty:
        with open(file_path, 'r') as json_file:
            data_list = json.load(json_file)
            return data_list
    else:
        raise FileNotFoundError


if __name__ == "__main__":
    main()
