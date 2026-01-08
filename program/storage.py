import os
import csv
from models import Operation

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "operations.csv")


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def save_operations(operations: list[Operation]):
    if operations is None:
        return

    ensure_data_dir()

    try:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ["amount", "category", "date", "comment", "type"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for op in operations:
                writer.writerow(op.to_dict())

    except (IOError, ValueError) as e:
        print(f"Ошибка при сохранении данных: {e}")


def load_operations() -> list[Operation]:
    operations = []

    if not os.path.exists(CSV_FILE):
        return operations

    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    op = Operation(
                        amount=float(row["amount"]),
                        category=row["category"],
                        date=row["date"],
                        comment=row.get("comment", ""),
                        op_type=row["type"]
                    )
                    operations.append(op)
                except ValueError as ve:
                    print(f"Пропущена некорректная запись: {ve}")

    except (IOError, csv.Error) as e:
        print(f"Ошибка при загрузке данных: {e}")

    return operations


def append_operation(operation: Operation):
    ensure_data_dir()

    file_exists = os.path.isfile(CSV_FILE)

    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            fieldnames = ["amount", "category", "date", "comment", "type"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(operation.to_dict())

    except (IOError, ValueError) as e:
        print(f"Ошибка при добавлении операции: {e}")