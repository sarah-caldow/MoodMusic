from MoodMusic import app
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from MoodMusic.application import anasense, keys, database, pyconnecter


user = '@matthewmercer' #twitter handle will be inputted by the user
genres = ["country", "pop", "rock", "jazz", "hip-hop", "indie"]
generated_songs = []
#first_song = True
#shows all entries in twitter
#***********************************************************
@app.route('/', methods=['GET','POST'])
def show_entries():
    db = database.get_db()
    #user = request.form["twitter"]
    entries = {}
    entries["tweets"] = anasense.getTweets(6, 20, user)
    entries["genres"] = genres
    spot_obj = pyconnecter.createSpotifyObject()
    cover_art = []
    current_song = []
    if (request.method == 'POST'):
        current_genres = []
        current_genres = request.form.getlist("current-genre")
        #sid = anasense.SentimentIntensityAnalyzer() is this needed?
        moodTag = anasense.determineMood(user)
        generated_songs = anasense.generateSongs(moodTag, current_genres)
        count = 0
        moodTag = anasense.determineMood(user)
        generated_songs = anasense.generateSongs(moodTag, current_genres)
        #first_song = False
        #else:
            #generated_songs.pop(0)
        for song in generated_songs:
            if (count==0):
                current_song.append("https://open.spotify.com/embed?uri=" + pyconnecter.listen(song[1],song[0],spot_obj))
            elif(count<=4):
                cover_art.append(pyconnecter.showCoverArt(song[1],song[0],spot_obj))
            else:
                break
            count += 1
        return render_template('show_entries.html', generated_songs = generated_songs, current_genres=current_genres, current_song = current_song[0], entries=entries, cover_art = cover_art, moodTag = moodTag)
    current_genres = ["none"]
    return render_template('show_entries.html', entries=entries, current_song = current_song, cover_art = cover_art)



#***********************************************************
'''@app.route('/genre', methods=['GET','POST'])
def genre():
    if (request.method == 'POST'):
        db = database.get_db()
        entries = {}
        entries["tweets"] = anasense.getTweets(6, 20)
        entries["genres"] = genres
        current_genre = request.form['current-genre']
        return render_template('show_entries.html', current_genre=current_genre, entries=entries)
'''

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
        #user = "@" + request.form["twitter"]
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
        return redirect(url_for('show_entries'), user = user)
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

def next_song():
    generated_songs.pop(0)
    return redirect(url_for('show_entries'))
