from collections import UserDict
from datetime import datetime
from exceptions import DuplicateEntry, ValueNotFound
from constants import BIRTHDAY_FORMAT, DATE_FORMAT


class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    def __str__(self):
        return str(self.value)

    def __eq__(self, __value: object) -> bool:
        self.value == __value


class Name(Field):
    def __init__(self, name: str) -> None:
        super().__init__(value=name)


class Phone(Field):
    def __init__(self, phone: str) -> None:
        if Phone.validate(phone):
            super().__init__(value=phone)

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value)

    @classmethod
    def validate(self, phone_number) -> bool:
        if len(phone_number) == 10 and phone_number.isdigit():
            return True
        else:
            raise ValueError("Invalid phone number!")


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @staticmethod
    def validate(d):
        try:
            datetime.strptime(d, BIRTHDAY_FORMAT)
            return True
        except ValueError:
            raise ValueError(f"Invalid date format! Expecting: {DATE_FORMAT}")


class Record:
    def __init__(self, name, birthday='') -> None:
        self.__name = Name(name)
        self.__phones = []
        self.add_birthday(birthday)

    @property
    def phones(self):
        return self.__phones

    @property
    def name(self):
        return self.__name
    
    @property
    def birthday(self):
        return self.__birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}" + "" if not self.birthday else f"birthday {self.birthday.strftime(BIRTHDAY_FORMAT)}"

    def with_phone_validation(func):
        def inner(self, phone: str):
            if Phone.validate(phone_number=phone):
                return func(self, phone)
        return inner

    @with_phone_validation
    def add_phone(self, phone: str):
        phone_record = self.find_phone(phone)
        if phone_record:
            raise DuplicateEntry(self.name, phone)
        else:
            self.phones.append(Phone(phone))

    def add_birthday(self, birthday: str):
        if birthday and Birthday.validate(birthday):
            self.__birthday = datetime.strptime(birthday, BIRTHDAY_FORMAT)
        else:
            self.__birthday = None

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
            else:
                raise ValueNotFound(phone=old_phone)

    @with_phone_validation
    def find_phone(self, phone: str) -> Phone:
        for p in self.phones:
            if p.value == phone:
                return p

    def __repr__(self) -> str:
        return f"name = {self.name}, phones: {'; '.join(p.value for p in self.phones)}, birthday = {self.birthday}"


class AddressBook(UserDict):

    def find(self, name: str) -> Record:
        '''finds record by username'''
        record = self.data.get(name)
        if not record:
            raise ValueNotFound(name=name)
        return record

    def delete(self, name: str):
        '''deletes record with the name from address book'''
        record = self.data.get(name)
        if not record:
            raise ValueNotFound(name=name)
        return self.data.pop(record.name.value)

    def add_record(self, record: Record):
        '''adds record to the address book'''
        self.data[record.name.value] = record

    def get_records(self):
        '''returs list of all records stored in the address book'''
        return self.data.values()


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # trying to create a phone with invalid input
    try:
        phone = Phone("924875643r")
        print(phone)
    except ValueError as e:
        print(e.args)

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # trying to create a record with an invalid birthday
    try:
        anna_record = Record("Anna", birthday='12/12/1999')
    except ValueError as e:
        print(e.args)

    # creating a record with a valid BD
    anna_record = Record("Anne", birthday='01.10.1980')
    anna_record.add_phone("9876543210")
    book.add_record(anna_record)

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    # jane_record.delete_phone("98235")  # -> Invalid phone number
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
    print(book)
