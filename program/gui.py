import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from models import Operation
from storage import load_operations, append_operation, save_operations
from utils import validate_date, validate_amount
from analysis import operations_to_df, plot_pie_by_category


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый планер")

        self.operations = load_operations()

        # --- Ввод операции ---
        tk.Label(root, text="Сумма").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Категория").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Дата (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        current_date = datetime.now().strftime("%Y-%m-%d")
        self.date_entry.insert(0, current_date)

        tk.Label(root, text="Комментарий").grid(row=3, column=0, padx=5, pady=5)
        self.comment_entry = tk.Entry(root)
        self.comment_entry.grid(row=3, column=1, padx=5, pady=5)

        self.type_var = tk.StringVar(value="expense")
        tk.Radiobutton(root, text="Расход", variable=self.type_var, value="expense").grid(row=4, column=0)
        tk.Radiobutton(root, text="Доход", variable=self.type_var, value="income").grid(row=4, column=1)

        tk.Button(root, text="Добавить операцию", command=self.add_operation).grid(row=5, column=0, columnspan=2,
                                                                                   pady=5)
        tk.Button(root, text="Анализ", command=self.analyze).grid(row=6, column=0, columnspan=2, pady=5)

        # --- Таблица для операций ---
        columns = ("date", "type", "category", "amount", "comment")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        self.tree.grid(row=0, column=2, rowspan=8, padx=10, pady=5)

        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("category", text="Категория")
        self.tree.heading("amount", text="Сумма")
        self.tree.heading("comment", text="Комментарий")

        self.tree.column("date", width=90, anchor="center")
        self.tree.column("type", width=70, anchor="center")
        self.tree.column("category", width=100)
        self.tree.column("amount", width=80, anchor="e")
        self.tree.column("comment", width=150)

        tk.Button(root, text="Удалить выделенное", command=self.delete_selected).grid(row=7, column=2, padx=10, pady=5)

        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Удалить", command=self.delete_selected)
        self.context_menu.add_command(label="Редактировать", command=self.edit_selected)

        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Delete>", lambda event: self.delete_selected())

        self.update_tree()

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_selected(self):
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите операцию для удаления")
            return

        if not messagebox.askyesno("Подтверждение", "Удалить выбранную операцию?"):
            return

        indices_to_delete = []
        for item in selected_items:
            item_index = self.tree.index(item)
            if 0 <= item_index < len(self.operations):
                indices_to_delete.append(item_index)

        indices_to_delete.sort(reverse=True)

        for index in indices_to_delete:
            self.operations.pop(index)

        save_operations(self.operations)
        self.update_tree()

        messagebox.showinfo("Готово", f"Удалено {len(selected_items)} операций")

    def edit_selected(self):
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите операцию для редактирования")
            return

        messagebox.showinfo("Информация", "Функция редактирования будет реализована в следующей версии")

    def add_operation(self):
        amount = self.amount_entry.get()
        date = self.date_entry.get()

        if not validate_amount(amount):
            messagebox.showerror("Ошибка", "Некорректная сумма")
            return

        if not validate_date(date):
            messagebox.showerror("Ошибка", "Некорректная дата")
            return

        try:
            op = Operation(
                float(amount),
                self.category_entry.get(),
                date,
                self.comment_entry.get(),
                self.type_var.get()
            )
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            return

        self.operations.append(op)
        append_operation(op)
        self.update_tree()
        messagebox.showinfo("Готово", "Операция добавлена")

        # Очистка полей после добавления
        self.clear_input_fields()

    def clear_input_fields(self):
        """Очищает все поля ввода, кроме даты"""
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.comment_entry.delete(0, tk.END)
        # Дата остается текущей - не очищаем
        # Радиокнопка остается на "расход" - не меняем

    def update_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for op in self.operations:
            self.tree.insert("", tk.END, values=(
                op.date.strftime("%Y-%m-%d"),
                op.op_type.upper(),
                op.category,
                f"{op.amount:.2f}",
                op.comment
            ))

    def analyze(self):
        df = operations_to_df(self.operations)
        plot_pie_by_category(df, "expense")
        plot_pie_by_category(df, "income")