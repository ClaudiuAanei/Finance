import json
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session
from website.report import ProcessFile

views = Blueprint('views',__name__)

SESSIONS_DATA = {}

@views.route('/', methods= ['GET','POST'])
def home_page():
    if request.method == 'POST':

        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            content = file.read().decode('utf-8')
            clean_file = ProcessFile(file= content, sep= ';', name= 'CLAUDIU AANEI')
            df = clean_file.get_last_month_tabel()
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')


            json_format = df.to_json(orient= 'records', date_format='iso', indent= 4)
            finances_tabel = json.loads(json_format)

            id_session = str(uuid.uuid4())

            SESSIONS_DATA[id_session] = finances_tabel
            session['id_session'] = id_session

            return redirect(url_for('views.finances'))

    return render_template('index.html')


@views.route('/finances')
def finances():
    finances_tabel = None
    id_session = session.get('id_session')

    if id_session and id_session in SESSIONS_DATA:
        finances_tabel = SESSIONS_DATA[id_session]

    return render_template('finances.html', tabel= finances_tabel)

@views.route('/apply_changes')
def save_changes():
    pass

