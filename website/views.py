import json
import uuid
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, session
from website.readfile import ProcessFile
from website.raportmaker import show_stats
from website.dateformat import change_date_format

views = Blueprint('views',__name__)

SESSIONS_DATA = {}


@views.route('/', methods= ['GET','POST'])
def home_page():
    global SESSIONS_DATA
    if request.method == 'POST':

        detinator = request.form.get('account_holder')
        date_format = request.form.get('date-format')

        start_date = change_date_format(request.form.get('start-date'), date_format)
        end_date = change_date_format(request.form.get('end-date'), date_format)

        separator = request.form.get('separator')
        file = request.files['file']

        if file and file.filename.endswith('.csv'):

            content = file.read().decode('utf-8')
            clean_file = ProcessFile(file= content, sep= separator[0], name= detinator, date_format= date_format)
            try:
                df = clean_file.get_tabel(first_date= start_date, last_date= end_date)
            except AttributeError:
                return redirect(url_for('views.home_page'))
            df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')

            json_format = df.to_json(orient= 'records', date_format='iso', indent= 4)
            finances_table = json.loads(json_format)

            with open('categories.json', mode='r', encoding='utf-8') as f:
                data = f.read()
                categories = json.loads(data)

            id_session = str(uuid.uuid4())

            SESSIONS_DATA[id_session] = [finances_table, categories]
            session['id_session'] = id_session

            return redirect(url_for('views.finances'))

    return render_template('index.html')


@views.route('/finances')
def finances():
    finances_table = None
    categories = None
    id_session = session.get('id_session')

    if id_session and id_session in SESSIONS_DATA:
        finances_table = SESSIONS_DATA[id_session][0]
        categories = SESSIONS_DATA[id_session][1]

    try:
        raport = SESSIONS_DATA[id_session][2]
    except IndexError:
        raport = None

    return render_template('finances.html', table= finances_table, categories= categories, raport=raport)


@views.route('/apply_changes', methods= ['GET', 'POST'])
def save_changes():

    if request.method == 'POST':
        categories = SESSIONS_DATA[session['id_session']][1]
        finances_table = SESSIONS_DATA[session['id_session']][0]

        categories = {key: [] for key in categories}

        for idx, row in enumerate(finances_table):
            category = request.form.get(f'category_{idx + 1}')
            if category and category != 'uncategorized':
                if row['Description'] not in categories.get(category, []):
                    categories.setdefault(category, []).append(row['Description'])

        for row in finances_table:
            for category in categories:
                if row['Description'] in categories[category]:
                    row['Category'] = category


    return redirect(url_for('views.finances'))


@views.route('/clear')
def clear_data():
    finances_table = SESSIONS_DATA[session['id_session']][0]
    categories = SESSIONS_DATA[session['id_session']][1]


    categories = {key: [] for key in categories}

    for row in finances_table:
        row['Category'] = 'uncategorized'

    SESSIONS_DATA[session['id_session']].clear()
    SESSIONS_DATA[session['id_session']] = [finances_table, categories]


    return redirect(url_for('views.finances'))


@views.route('/delete', methods= ['GET','POST'])
def delete():
    if request.method == 'POST':

        finances_table = SESSIONS_DATA[session['id_session']][0]
        selected_rows = request.form.getlist('selected_rows')

        if selected_rows:
            for i in reversed(selected_rows):
                finances_table.pop(int(i) - 1)

            SESSIONS_DATA[session['id_session']][0] = finances_table

    return redirect(url_for('views.finances'))


@views.route('/stats')
def generate_stats():
    data = SESSIONS_DATA[session['id_session']][0]
    df = pd.DataFrame(data)
    df.to_csv('formated.csv', index= False)
    SESSIONS_DATA[session['id_session']].insert(2, show_stats(df))
    return redirect(url_for('views.finances'))