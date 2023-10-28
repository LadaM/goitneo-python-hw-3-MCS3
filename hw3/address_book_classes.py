from collections import UserDict
from exceptions import ValueNotFound


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name: str) -> None:
        super().__init__(value=name)


class Phone(Field):
    def __init__(self, phone: str) -> None:
        super().__init__(value=phone)

    @classmethod
    def validate(self, phone_number) -> bool:
        return len(phone_number) == 10 and phone_number.isdigit()


class Record:
    def __init__(self, name) -> None:
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def with_phone_validation(func):
        def inner(self, phone: str):
            if Phone.validate(phone_number=phone):
                return func(self, phone)
            else:
                print("Invalid phone number!")
        return inner

    @with_phone_validation
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    @with_phone_validation
    def delete_phone(self, phone: str):
        to_remove = self.find_phone(phone)
        self.phones.remove(to_remove)

    def edit_phone(self, old_phone: str, new_phone: str):
        if Phone.validate(new_phone):
            to_remove = self.find_phone(old_phone)
            if to_remove:
                self.phones.remove(to_remove)
                self.phones.append(Phone(new_phone))

    @with_phone_validation
    def find_phone(self, phone: str) -> Phone:
        for p in self.phones:
            if p.value == phone:
                return p


class AddressBook(UserDict):

    def find(self, name: str) -> Record:
        '''finds record by username'''
        record = self.data.get(name)
        if not record:
            raise ValueNotFound(name)
        return record

    def delete(self, name: str):
        '''deletes record with the name from address book'''
        record = self.data.get(name)
        if not record:
            raise ValueNotFound(name)
        return self.data.pop(record.name.value)

    def add_record(self, record: Record):
        '''adds record to the address book'''
        self.data[record.name.value] = record


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
    jane_record.delete_phone("98235")  # -> Invalid phone number
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # deleting the phone from record
    john.delete_phone(found_phone.value)
    print(john)  # phones: 1112223333

    # Видалення запису Jane
    book.delete("Jane")
    print(len(book))  # -> 1
