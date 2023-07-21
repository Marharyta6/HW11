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
        # if len(new_value) != 13 or not new_value.startswith("+38"):
        #     raise ValueError("Invalid phone number")
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
    def __init__(self, name: Name,
                 phone: Phone = None,
                 birthday: Birthday = None) -> None:
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

    def days_to_birthday(self, birthday: Birthday):
        #birthday = self.birthday
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

    def iterator(self, rec_per_page=3):
        record_counter = 0
        result = ""
        for record in self.values():
            result += str(record) + '\n'
            record_counter += 1
            if record_counter >= rec_per_page:
                yield result
                record_counter = 0
                result = ""
        if result:
            yield result

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
