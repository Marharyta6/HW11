from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)

class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, new_value):
        if len(new_value) != 13 or not new_value.startswith("+38"):
            raise ValueError("Invalid phone number")
        self._value = new_value


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid birthday format")
        self._value = new_value

    @property
    def date(self):
        return datetime.strptime(self.value, "%d-%m-%Y").date()


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"
    
    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(
                today.year, self.birthday.date.month, self.birthday.date.day).date()
            if next_birthday < today:
                next_birthday = datetime(
                    today.year + 1, self.birthday.date.month, self.birthday.date.day).date()
            days_left = (next_birthday - today).days
            return f"Days until the next birthday of {self.name}: {days_left}"
        else:
            return f"No birthday set for contact {self.name}"

    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}, {self.birthday}"
    

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)

    return wrapper


address_book = AddressBook()


@input_error
def add_contact(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    birthday = Birthday(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone, birthday)
    return address_book.add_record(rec)


@input_error
def change_phone(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


@input_error
def get_phone(*args):
    name = Name(args[0])
    #record = Record(name)
    rec: Record = address_book.get(str(name))
    if rec:
        return f"The phone number(s) for '{name}' is/are: {', '.join(str(p) for p in rec.phones)}."
    else:
        raise KeyError(f"Contact '{name}' not found.")


@input_error
def show_all_contacts(*args):
    return address_book
    # if not address_book.data:
    #     return "There are no contacts saved."

    # result = ""
    # for name, record in address_book.data.items():
    #     phone_numbers = ", ".join(record.phones)
    #     result += f"{name}: {phone_numbers}\n"

    #return result


def greeting_command(*args):
    return "How can I help you?"


def exit_command(*args):
    return "Good bye!"


def unknown_command(*args):
    return "Invalid command. Please try again."


COMMANDS = {add_contact: ("add", ),
            change_phone: ("change",),
            get_phone: ("phone",),
            show_all_contacts: ("show all", ),
            greeting_command: ("hello", ),
            exit_command: ("good bye", "close", "exit")
            }


def parser(user_input):
    for command, kwds in COMMANDS.items():
        for kwd in kwds:
            if user_input.lower().startswith(kwds):
                return command, user_input[len(kwd):].strip().split()
    return unknown_command, []


def main():
    # print("How can I help you?")
    while True:
        user_input = input(">>>")

        func, data = parser(user_input)

        print(func(*data))

        if func == exit_command:
            break


if __name__ == "__main__":
    main()
    # rec1 = Record("Bill","0997663","2020-10-15")
    # print(rec1)
    
