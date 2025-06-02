import pandas as pd
import plotly.express as px
import plotly.io as pio


def show_stats(df):

    stats = {
        "income": float(df[df.Category == "income"]['Amount'].sum()),
        "savings": float(round(df['Amount'].sum(), 2)),
        "housing": float(round(df[df.Category == 'housing']['Amount'].sum(), 2)),
        "bankLoans": float(round(df[df.Category == 'bank loans']['Amount'].sum(), 2)),
        "groceries": float(round(df[df.Category == 'groceries']['Amount'].sum(), 2)),
        "mobility": float(round(df[df.Category == 'mobility']['Amount'].sum(), 2)),
        "utilities": float(round(df[df.Category == 'utilities & telecom']['Amount'].sum(), 2)),
        "insurances": float(round(df[df.Category == 'finance & insurances']['Amount'].sum(), 2)),
        "health": float(round(df[df.Category == 'health']['Amount'].sum(), 2)),
        "restaurants": float(round(df[df.Category == 'bars & restaurants']['Amount'].sum(), 2)),
        "shopping": float(round(df[df.Category == 'shopping']['Amount'].sum(), 2)),
        "education": float(round(df[df.Category == 'education']['Amount'].sum(), 2)),
        "entertainment": float(round(df[df.Category == 'leisure & entertainment']['Amount'].sum(), 2)),
        "services": float(round(df[df.Category == 'services']['Amount'].sum(), 2)),
        "atmWithdraw": float(round(df[df.Category == 'atm withdraw']['Amount'].sum(), 2)),
        "government": float(round(df[df.Category == 'government']['Amount'].sum(), 2)),
        "others": float(round(df[df.Category == 'others']['Amount'].sum(), 2)),
    }

    expenses = {k: abs(v) for k, v in stats.items() if k not in ["income", "savings"] and v != 0}

    data = pd.DataFrame(list(expenses.items()), columns=["Category", "Amount"])
    data["Category"] = data["Category"].str.title()

    fig = px.bar(data, x="Category", y="Amount",
                 title="Expense Distribution by Category",
                 labels={"Category": "Category", "Amount": "Amount (EUR)"},
                 text="Amount",
                 color="Category",
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 height= 800)

    fig.update_traces(texttemplate='%{text}', textposition='outside', hoverinfo='x+y+text')
    fig.update_xaxes(tickangle=45)

    income_color = 'green' if stats['income'] > 0 else 'red'
    savings_color = 'green' if stats['savings'] > 0 else 'red'

    fig.update_layout(
        annotations=[
            dict(
                x=0.9, y=0.9,
                xref="paper", yref="paper",
                text=f"Income: {stats['income']} EUR",
                showarrow=False,
                font=dict(size=14, color=income_color),
                align="left"
            ),
            dict(
                x=0.9, y=0.85,
                xref="paper", yref="paper",
                text=f"Savings: {stats['savings']} EUR",
                showarrow=False,
                font=dict(size=14, color=savings_color),
                align="left"
            )
        ]
    )

    return pio.to_html(fig, full_html=False)