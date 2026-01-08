import sys
import unittest
from datetime import datetime

sys.path.insert(0, r"C:\Users\antar\PycharmProjects\Financial_planning\program")

from models import Operation


class TestOperation(unittest.TestCase):

    def test_to_dict(self):
        op = Operation(100, "Food", "2025-12-27", "Test comment", "expense")
        d = op.to_dict()
        self.assertEqual(d["amount"], 100)
        self.assertEqual(d["category"], "Food")
        self.assertEqual(d["date"], "2025-12-27")
        self.assertEqual(d["comment"], "Test comment")
        self.assertEqual(d["type"], "expense")

    def test_date_conversion(self):
        op = Operation(50, "Salary", "2025-12-30", "Monthly", "income")
        self.assertIsInstance(op.date, datetime)
        self.assertEqual(op.date.strftime("%Y-%m-%d"), "2025-12-30")

        # Тест с комментарием но без указания типа
        op2 = Operation(300, "Shopping", "2025-12-29", "New shop")
        self.assertEqual(op2.amount, 300)
        self.assertEqual(op2.category, "Shopping")
        self.assertEqual(op2.comment, "New shop")
        self.assertEqual(op2.op_type, "expense")

    def test_number_format_with_comma(self):
        """Тест что в числах нельзя использовать запятую как разделитель"""
        # Запятая вместо точки должна вызывать ошибку
        with self.assertRaises(ValueError):
            Operation("100,50", "Food", "2025-12-27", "Amount with comma")

        # Но точка должна работать
        op_with_dot = Operation("100.50", "Food", "2025-12-27", "Amount with dot")
        self.assertEqual(op_with_dot.amount, 100.5)

        # Целое число должно работать
        op_int = Operation("100", "Food", "2025-12-27", "Integer as string")
        self.assertEqual(op_int.amount, 100.0)


if __name__ == "__main__":
    unittest.main()