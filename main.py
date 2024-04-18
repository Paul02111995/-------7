from datetime import datetime, timedelta
from address_book import AddressBook, Record
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
        if record.birthday:
            birthday = record.birthday.value
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=birthday_this_year.year + 1)
            days_to_birthday = (birthday_this_year - today).days
            if 0 <= days_to_birthday <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() >= 5:
                    days_until_monday = (7 - congratulation_date.weekday()) % 7
                    congratulation_date += timedelta(days=days_until_monday)

                birthday_list.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
                })

    if birthday_list:
        result = "\n".join([f"{user['name']}: {user['congratulation_date']}" for user in birthday_list])
        return f"Upcoming birthdays in the next week:\n{result}"
    else:
        return "No birthdays in the next week."
     
@input_error
def change_phone(args, book):
    if len(args) != 3:
        return "Invalid command. Please provide name, old phone number, and new phone number after 'change'."
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        try:
            if old_phone not in [phone.value for phone in record.phones]:
                return f"Error: Old phone number {old_phone} not found for {name}."
            
            record.edit_phone(old_phone, new_phone)
            return f"Phone number updated for {name}."
        except ValueError as e:
            return f"Error: {str(e)}"
    else:
        return f"Contact {name} not found."


@input_error
def show_phone(args, book):
    if len(args) != 1:
        return "Invalid command. Please provide a name after 'phone'."
    
    name = args[0]
    record = book.find(name)
    
    if record:
        phone_numbers = [str(phone) for phone in record.phones]
        return f"{name}'s phone number is {', '.join(phone_numbers)}."
    else:
        return f"Contact {name} not found."

@input_error
def show_all_contacts(book: AddressBook):
    contacts = []
    for record in book.data.values():
        contacts.append(str(record))
    return "\n".join(contacts) if contacts else "Address book is empty."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        
        if not user_input:
            print("Command not entered. Please enter a command.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()