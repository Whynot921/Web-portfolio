from flask import Flask, render_template, url_for, request, session, redirect, flash, abort, g
import os
import sqlite3
from Fdatabase import Fdatabase
app = Flask(__name__)

DEBUG = True
SECRET_KEY='sdfsdfsdfsdfsdilvihnih'
DATABASE="/tmp/Accounts.db"

app.config.from_object(__name__)
app.config.update(dict(DATABASE='Accounts.db'))

def connect_db():
    conn=sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

def images():
    db=get_db()
    dbase = Fdatabase(db)
    return dbase.get_file(session['userLogged'])

@app.route('/profile/<name>', methods=['POST','GET'])
def profile(name):
    if 'userLogged' not in session or session['userLogged'] != name:
        abort(401)
    db=get_db()
    dbase = Fdatabase(db)               
    if request.method == 'POST':
        if 'todel' not in request.form:
            file = request.files['file'].read()
            dbase.add_file(name,file)
        elif request.form['todel'] != '':
            dbase.delete_file(request.form['todel'],session['userLogged'])
    return render_template('logged.html', images=dbase.get_file(session['userLogged']))

@app.route('/profile')
def ds():
    if 'userLogged' in session:
        return redirect(url_for('profile', name=session['userLogged']))
    else:
        return redirect('/')

@app.route('/t.html')
@app.route('/', methods=['POST','GET'])
def login():
    db=get_db()
    dbase = Fdatabase(db)
    Accountsdict = dbase.get_data()
    if 'userLogged' in session:
        return redirect(url_for('profile', name=session['userLogged']))
    elif request.method == 'POST':
        if 'reg' not in request.form and request.form['name'] in Accountsdict.keys():
            if request.form['password'] == Accountsdict[request.form['name']]:
                session['userLogged'] = request.form['name']   
                return redirect(url_for('profile',name=session['userLogged']))
            else:
                flash('Неверный пароль!')
        elif 'reg' in request.form:
            if request.form['name'] not in Accountsdict.keys():
                if len(request.form['password']) > 3:
                    dbase.add_data(username=request.form['name'],password=request.form['password'])
                else:
                    flash('Пароль должен быть длиннее 3-ёх символов ')
            else:
                flash('Это имя занято')
        else:
            flash('Аккаунта с таким именем не существует!')

    
    
    return render_template('t.html')

@app.route('/about')
def about():
    return "<h1>О сайте</h1>"

@app.route("/profile/leave")
def leave():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)