from flask import (Flask, request, render_template,
                   session, flash, redirect, url_for)
from vocabx import details
from forms import RegistrationForm
from functools import wraps
import MySQLdb
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
import gc
from flask_bootstrap import Bootstrap
from dbconnect import connection

app = Flask(__name__)
app.config['SECRET_KEY'] = "iamBoring"
Bootstrap(app)
# @app.route('/?query=<string:word>', methods=['GET', 'POST'])


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@app.route('/index/')
def index(word=None):
    #flash('Hey There!', "success")
    word = request.args.get('query')
    if word == None:
        word = 'welcome'
    dict = details(word)
    return render_template('index.html', word=word, values=dict)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(405)
def method_not_found(e):
    return render_template('405.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    try:
        c, conn = connection()

        error = None
        if request.method == 'POST':

            data = c.execute("SELECT * FROM users WHERE username = '%s'"%
                             thwart(request.form['username']))
            data = c.fetchone()[2]

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                flash('You are now logged in as '+ str(session['username']), 'success')
                return redirect(url_for('index'))

            else:
                error = 'Invalid credentials. Try again'
        gc.collect()
        return render_template('login.html', error=error)
    except Exception as e:
        error = 'Invalid credentials. Try again'
        return render_template('login.html', error=error)


@app.route('/check/')
def check():
    c, conn = connection()
    return 'okay'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    try:
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            #flash("register attempted")

            username = form.username.data
            email = form.email.data

            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = '%s'" %
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another", 'warning')
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email)))
                conn.commit()
                flash('Congrats! You\'ve been registered successfully!', 'success')
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
        gc.collect()
        #flash("hi there.")
        return render_template('register.html', form=form)
    except Exception as e:
        return(str(e))


@login_required
@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	session.clear()
	flash('You have been logged out.', 'success')
	gc.collect()
	return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
