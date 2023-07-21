from classes import AddressBook, Name, Phone, Record, Birthday



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
    phone = Phone(args[1]) if len(args) > 2 else None
    birthday = Birthday(args[2]) #if len(args) > 3 else None
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
    pages = int(args[0]) if args else None
    if pages:
        result = ""
        for page, recs in enumerate(address_book.iterator(pages), 1):
            result += f"page {page} :\n{recs}"
        return result
    return address_book

@input_error
def get_birthday(*args):
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.days_to_birthday(name)
    else:
        raise KeyError(f"Contact '{name}' not found.")


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
            get_birthday: ("birthday", ),
            greeting_command: ("hello", ),
            exit_command: ("good bye", "close", "exit"),
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
    # for _ in range(10):
    #     rec1 = Record(Name(f"Bill_{_}"),Phone("+380997663345"),Birthday("20-10-2015"))
    #     address_book.add_record(rec1)
    main()
