from MoodMusic import app
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from MoodMusic.application import anasense, keys, database

genres = ["pop", "rock", "jazz", "80's", "90's", "hip hop", "party", "blues"]

#shows all entries in twitter 
#***********************************************************
@app.route('/')
def show_entries():
    db = database.get_db()
    entries = {}
    entries["tweets"] = anasense.getTweets(6, 20)
    entries["genres"] = genres
    return render_template('show_entries.html', entries=entries)

#***********************************************************

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

