import pandas as pd
import plotly.express as px
import plotly.io as pio


def generate_expense_report(df: pd.DataFrame) -> str:
    """
    Generates an interactive expense report from a DataFrame.

    This function takes a pandas DataFrame containing financial transactions,
    groups them by category, and calculates the total amount for each. It
    differentiates between income and expenses, calculates total savings, and
    creates a Plotly bar chart to visualize the expense distribution. The chart
    includes annotations for total income and savings.

    Args:
        df (pd.DataFrame): A DataFrame that must include 'Category' and 'Amount'
                           columns. Income is expected to be a positive value,
                           while expenses should be negative.

    Returns:
        str: An HTML string representing the Plotly chart, ready to be
             embedded in a web page. The returned HTML is a fragment, not a
             full document.
    """
    # 1. Dynamically calculate the sum for each category
    category_totals = df.groupby('Category')['Amount'].sum()

    # 2. Extract income and calculate total expenses
    # Assumes 'income' is a category name. Defaults to 0 if not found.
    income = category_totals.get('income', 0)

    # All other categories are treated as expenses
    expenses = category_totals[category_totals.index != 'income'] * -1

    # Filter out any credits/refunds to only sum true expenses
    expenses = expenses[expenses > 0]

    # 3. Calculate savings
    total_expenses = expenses.sum()
    savings = income - total_expenses

    # 4. Prepare the data for plotting
    expenses_df = expenses.reset_index()
    expenses_df.columns = ['Category', 'Amount']
    expenses_df = expenses_df.sort_values(by='Amount', ascending=False)

    # Ensure consistent title case for display
    expenses_df['Category'] = expenses_df['Category'].str.title()

    # 5. Create the bar chart
    fig = px.bar(expenses_df,
                 x="Category",
                 y="Amount",
                 title="Expense Distribution by Category",
                 labels={"Category": "Category", "Amount": "Amount (EUR)"},
                 text_auto='.2f',  # Automatically display the value on the bar, formatted to 2 decimal places
                 color="Category")

    fig.update_traces(textposition='outside')
    fig.update_xaxes(tickangle=45)
    fig.update_layout(height=800, showlegend=False)

    # 6. Add annotations for key metrics
    income_color = 'green' if income > 0 else 'red'
    savings_color = 'green' if savings > 0 else 'red'

    fig.update_layout(
        annotations=[
            dict(
                x=0.95, y=0.95, xref="paper", yref="paper",
                text=f"Income: {income:.2f} EUR", showarrow=False,
                font=dict(size=14, color=income_color), align="right"
            ),
            dict(
                x=0.95, y=0.90, xref="paper", yref="paper",
                text=f"Savings: {savings:.2f} EUR", showarrow=False,
                font=dict(size=14, color=savings_color), align="right"
            )
        ]
    )

    return pio.to_html(fig, full_html=False, config={'displayModeBar': False})


# This part allows the script to be run directly for testing purposes
if __name__ == '__main__':
    # Example usage with sample data
    sample_data = {
        'Category': ['income', 'housing', 'groceries', 'transport',
                     'utilities', 'shopping', 'entertainment', 'subscriptions'],
        'Amount': [3500.00, -850.50, -475.25, -150.00, -210.75, -400.00, -180.50, -45.00]
    }
    sample_df = pd.DataFrame(sample_data)

    # Generate the report HTML
    html_chart = generate_expense_report(sample_df)

    # Save the output to an HTML file to view it
    with open("expense_report.html", "w", encoding="utf-8") as f:
        f.write(html_chart)

    print("Report generated successfully!")