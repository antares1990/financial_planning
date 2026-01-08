import pandas as pd
import matplotlib.pyplot as plt


def operations_to_df(operations):
    if not operations:
        return pd.DataFrame()

    data = [op.to_dict() for op in operations]
    df = pd.DataFrame(data)

    return df


def group_by_category(df, op_type):
    if df.empty:
        return pd.Series(dtype=float)

    filtered = df[df["type"] == op_type]

    if filtered.empty:
        return pd.Series(dtype=float)

    result = filtered.groupby("category")["amount"].sum()

    return result


def plot_pie_by_category(df, op_type):
    if df.empty:
        return

    data = group_by_category(df, op_type)

    if data.empty:
        return

    total = data.sum()

    def format_autopct(pct):
        value = pct * total / 100.0
        return f'{pct:.1f}%\n({value:.2f} руб.)'

    type_names = {
        'expense': 'Расходы',
        'income': 'Доходы'
    }
    title = type_names.get(op_type, op_type)

    plt.figure(figsize=(10, 8))
    plt.pie(data.values, labels=data.index, autopct=format_autopct, startangle=90)
    plt.title(f'Распределение {title} по категориям (Всего: {total:.2f} руб.)', fontsize=14, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()