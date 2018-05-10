from flask import Flask,request, render_template

app = Flask(__name__)


@app.route('/')
def welcome(word=None):
    word = request.args.get('query')
    if word==None:
        word = 'welcome'
    return render_template('index.html', word = word)


if __name__ == '__main__':
    app.run(debug=True, port=7000)
