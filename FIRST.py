from flask import Flask, render_template, url_for, request, session, redirect, flash, abort, g, send_file
import sqlite3
import os
import re
from Fdatabase import Fdatabase
app = Flask(__name__)

DEBUG = True
SECRET_KEY='sdfsdfsdfsdfsdilvihnih'
DATABASE="/tmp/Accounts.db"
regex = "^[a-zA-ZА-Яа-яёЁ0123456789_]+$"
pattern = re.compile(regex)

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
        if 'file' in request.files:
            file = request.files['file'].read()
            flag = False
            if file != b'':
                dbase.add_file(name,file)
        if 'Download' in request.form and request.form['num'] != 0:
            file = dbase.get_file(name,request.form['num'])
            return send_file(file, as_attachment=True, download_name=f'img{request.form['num']}.png', mimetype=f'img{request.form['num']}/png")
        elif 'Delete' in request.form and request.form['num'] != 0:
            dbase.delete_file(request.form['num'], name)

    return render_template('logged.html', images=dbase.get_file(name))

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
            if request.form['name'] not in Accountsdict.keys() and (pattern.search(request.form['name']) is not None):
                if len(request.form['password']) > 3 and (pattern.search(request.form['password']) is not None) and dbase.add_data(request.form['name'], request.form['password']) :
                    session['userLogged'] = request.form['name']
                    return redirect(url_for('profile',name=session['userLogged']))
                else:
                    flash('Пароль должен быть длиннее 3-ёх символов и состоять из допустимых символов ')
            else:
                flash('Это имя занято или оно состоит из недопустимых символов')
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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)
