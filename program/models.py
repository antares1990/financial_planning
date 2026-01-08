from datetime import datetime


class Operation:
    def __init__(self, amount, category, date, comment="", op_type="expense"):
        # Проверяем содержит ли сумма запятую
        if isinstance(amount, str) and ',' in amount:
            raise ValueError(
                f"Некорректная сумма: '{amount}'. "
                "Используйте точку как разделитель десятичных дробей (например: 100.50)"
            )

        try:
            self.amount = float(amount)
        except (ValueError, TypeError):
            raise ValueError(f"Некорректная сумма: '{amount}'. Ожидается число.")

        self.category = category

        try:
            self.date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Некорректный формат даты: '{date}'. Используйте YYYY-MM-DD.")

        self.comment = comment
        self.op_type = op_type

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date.strftime("%Y-%m-%d"),
            "comment": self.comment,
            "type": self.op_type
        }