from flask import Flask, request, render_template
from vocabx import details
app = Flask(__name__)

# @app.route('/?query=<string:word>', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def welcome(word=None):
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

if __name__ == '__main__':
    app.run(debug=True, port=7000)
