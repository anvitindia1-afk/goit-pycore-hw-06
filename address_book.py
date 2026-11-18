# Адресна книга на класах: Field, Name, Phone, Record, AddressBook.

from collections import UserDict


class Field:
    """Базовий клас для всіх полів запису (ім'я, телефон тощо)."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Ім'я контакту — обов'язкове поле, тому не може бути порожнім."""

    def __init__(self, value):
        if not value:
            raise ValueError("Name is required.")
        super().__init__(value)   # далі працює як звичайний Field


class Phone(Field):
    """Номер телефону — рівно 10 цифр."""

    def __init__(self, value):
        # isdigit() — чи всі символи цифри; len() — скільки їх
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Record:
    """Один контакт: ім'я та список телефонів."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []          # тут лежать об'єкти Phone

    def add_phone(self, phone):
        """Додає телефон (Phone сам перевірить, що там 10 цифр)."""
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        """Шукає телефон у списку. Повертає об'єкт Phone або None."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone):
        """Видаляє телефон зі списку."""
        p = self.find_phone(phone)
        if p is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        """Замінює старий телефон на новий."""
        p = self.find_phone(old_phone)
        if p is None:
            raise ValueError(f"Phone {old_phone} not found.")
        # Спершу створюємо новий Phone — якщо номер неправильний,
        # буде помилка, і старий номер залишиться на місці
        new_p = Phone(new_phone)
        index = self.phones.index(p)   # на якому місці стоїть старий номер
        self.phones[index] = new_p

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """
    Адресна книга. UserDict — це "словник", який ми можемо доповнити своїми методами.
    Записи лежать у self.data: ключ — ім'я, значення — Record.
    """

    def add_record(self, record):
        """Додає запис у книгу."""
        self.data[record.name.value] = record

    def find(self, name):
        """Повертає запис за іменем або None, якщо такого немає."""
        return self.data.get(name)

    def delete(self, name):
        """Видаляє запис за іменем (якщо він є)."""
        if name in self.data:
            del self.data[name]


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
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
