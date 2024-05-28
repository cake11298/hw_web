from flask import Flask, request, render_template, redirect, url_for, session, g, flash
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20)

DATABASE = 'data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False, commit=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    if commit:
        get_db().commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = session.get('username')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM user WHERE username = ? AND password = ?', [username, password], one=True)
        if user:
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login', error='true'))
    error = request.args.get('error')
    return render_template('login.html', error=error, username=username if username else '訪客')

@app.route('/register', methods=['GET', 'POST'])
def register():
    username = session.get('username')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        query_db('INSERT INTO user (username, password, email, phone) VALUES (?, ?, ?, ?)', 
                 [username, password, email, phone], commit=True)
        return redirect(url_for('login'))
    return render_template('register.html', username=username if username else '訪客')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def get_articles():
    query = "SELECT title, content, publisher, date, tag FROM article"
    articles = query_db(query)
    return articles

@app.route('/inner-page')
def innerpage():
    username = session.get('username')
    category = request.args.get('tag', 'all')  
    if category == 'all':
        query = "SELECT * FROM article"
    else:
        query = "SELECT * FROM article WHERE tag = ?"

    articles = query_db(query, [category]) if category != 'all' else query_db(query)
    articles_data = [
        {
            "title": article['title'],
            "content": article['content'],
            "publisher": article['publisher'],
            "tag": article['tag'],
            "date": article['date'],
            "link": "blog-article.html"
        } for article in articles
    ]
    return render_template('inner-page.html', username=username, articles=articles_data)

@app.route('/')
def index():
    username = session.get('username')
    return render_template('index.html', username=username if username else '訪客')

if __name__ == '__main__':
    app.run(debug=True)
