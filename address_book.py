from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits")

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, number):
        self.phones.append(Phone(number))

    def remove_phone(self, number):
        updated_phones = []
        for phone in self.phones:
            if phone.value != number:
                updated_phones.append(phone)
        self.phones = updated_phones

    def edit_phone(self, old_number, new_number):
        if not any(phone.value == old_number for phone in self.phones):
            raise ValueError("Old phone number is not exist")    
        
        if len(new_number) != 10 or not new_number.isdigit():
            raise ValueError("New phone number must be 10 digits")
        
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                break

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None
    
    def add_birthday(self, value):
        if self.birthday is None:
            self.birthday = Birthday(value)
        else:
            raise ValueError("Only one birthday is allowed per record.")

    def __str__(self):
        phones = "; ".join([phone.value for phone in self.phones])
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {str(e)}"
    return wrapper

def parse_input(user_input):
    return user_input.split()

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday}."
    else:
        return f"Contact {name} not found or birthday not set."

@input_error
def birthdays(args, book):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    birthday_list = []
    for record in book.data.values():
        if record.birthday and record.birthday.value >= today and record.birthday.value <= next_week:
            birthday_list.append((record.name.value, record.birthday.value))
    if birthday_list:
        result = "\n".join([f"{name}: {birthday}" for name, birthday in birthday_list])
        return f"Birthdays in the next week:\n{result}"
    else:
        return "No birthdays in the next week."

@input_error
def change_phone(args, book):
    name, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(new_phone)
        return f"Phone number updated for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}'s phone number is {', '.join(record.phones)}."
    else:
        return f"Contact {name} not found."

@input_error
def show_all_contacts(book):
    if book:
        return "\n".join([str(record) for record in book.data.values()])
    else:
        return "No contacts found."