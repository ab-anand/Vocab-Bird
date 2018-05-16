from flask import Flask, request, render_template
from vocabx import details
from forms import RegistrationForm
from functools import wraps
import MySQLdb
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
import gc
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
# @app.route('/?query=<string:word>', methods=['GET', 'POST'])


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/')
def index(word=None):
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


@app.route('/login/', methods=['GET','POST'])
def login():
    return render_template('login.html')


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

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))
                conn.commit()
                flash('Thanks for registering')
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


if __name__ == '__main__':
    app.run(debug=True, port=7000)
