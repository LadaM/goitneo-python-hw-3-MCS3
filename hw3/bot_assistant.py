from pathlib import Path
from constants import COMMANDS, CONTACTS_FILE
from exceptions import ValueNotFound, InvalidCommand, DuplicateEntry
from address_book_classes import AddressBook, Record


def main():
    print("Welcome to the assistant bot!")
    # here look for the file with previously stored contacts -> load it if it exists
    # creating a new address book #TODO populate with retrieved data
    contacts = AddressBook()
    while True:
        command = input("Enter a command: ").strip().lower()
        try:
            if command == "hello":
                print("How can I help you?")
            elif command.startswith("add-birthday"):
                try:
                    _, name, birthday = command.split(' ')
                    msg = add_birthday(name, birthday, contacts)
                    print(msg)
                except ValueError:
                    raise InvalidCommand(COMMANDS.get('add-birthday'))
            elif command.startswith("add"):
                try:
                    _, name, phone = command.split(' ')
                    msg = add_contact(name, phone, contacts)
                    print(msg)
                except ValueError:
                    raise InvalidCommand(COMMANDS.get('add'))
            elif command.startswith("change"):
                try:
                    _, name, old, new = command.split(' ')
                    msg = update_contact(
                        name, old_phone=old, new_phone=new, contacts=contacts)
                    print(msg)
                except ValueError:
                    raise InvalidCommand(COMMANDS.get('update'))
            elif command.startswith("phone"):
                try:
                    _, name = command.split(' ')
                    record = get_phone(name, contacts)
                    print(record)
                except ValueError:
                    raise InvalidCommand(COMMANDS.get('phone'))
            elif command.startswith("all"):
                msg = show_all_contacts(contacts)
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
        except ValueError as e:
            return e.args[0]
        except DuplicateEntry as error:
            return f"We alreay have an entry with name {error.name} and phone {error.phone}"
        except ValueNotFound as error:
            return f"Phone {error.phone} wasn't found in our records!" if error.phone else f"No contact for name {error.name} found"
        except FileNotFoundError:
            # if the file is empty there are no contacts to show
            return "We haven't stored any contacts yet"
    return inner


@input_error
def add_contact(name: str, phone: str, contacts: AddressBook):
    try:
        # if we already have a name in our contact list, we add a phone number to the record
        record = contacts.find(name)
        record.add_phone(phone)
    except ValueNotFound:
        new_record = Record(name)
        new_record.add_phone(phone)
        print(new_record)
        contacts.add_record(record=new_record)
    return "Contact added"

@input_error
def add_birthday(name: str, birthday: str, contacts: AddressBook):
    record = contacts.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added"


@input_error
def update_contact(name, old_phone, new_phone, contacts: AddressBook):
    record = contacts.find(name)
    record.edit_phone(old_phone=old_phone, new_phone=new_phone)
    return "Contact updated"


@input_error
def get_phone(name, contacts: AddressBook):
    return contacts.find(name)


@input_error
def show_all_contacts(contacts: AddressBook):
    print('\n'.join([str(record) for record in contacts.get_records()]))  # TODO prettify the output
    # return '\n'.join(contacts.values())


if __name__ == "__main__":
    main()
