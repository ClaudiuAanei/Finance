# FinanceTracker

This application provides a simple interface to upload a CSV file, process the transaction data using a powerful backend, and visualize spending habits through interactive charts.

Finance Tracker 📊
A simple web app to upload and analyze your bank statement from a CSV file.

Note: This project is a learning exercise and my first application built with the Flask framework. It should be considered a work in progress. As such, features like comprehensive exception handling have not yet been implemented.


## ✨ Key Features
CSV Upload: Add your bank statement directly from the browser, with support for various date formats and separators.

Transaction Categorization: Assign categories to your expenses and income for better organization.

Easy Editing: Modify or delete transactions directly within the table.

Visual Report: Generate an interactive chart to visualize your spending distribution and a summary of your finances.

Light/Dark Theme: Change the interface appearance for your visual comfort.

## 🚀 How It Works
* Upload: Fill out the form on the main page and upload your .csv file.

* Categorize: Edit the categories directly in the displayed table and click "Apply Changes" to save.

* Analyze: Click "Show Report" to generate and view the expense chart.

🛠️ Technologies
* Backend: Python, Flask
* Data Processing: Pandas
* Charting: Plotly
* Frontend: HTML, Bootstrap 5


### To get this project up and running on your local machine, follow these steps.

1. Clone the repository

* On macOS/Linux:

        python3 -m venv venv
        source venv/bin/activate
* On Windows:

        python -m venv venv
        .\venv\Scripts\activate

2. Install the required packages

    
    pip install -r requirements.txt
    Run the application

On macOS/Linux:

    export FLASK_APP=website
    flask run

On Windows:

    set FLASK_APP=website
    flask run

Run the application from:

    app.py

If you want to see how it works in folder try_file you have a .csv
