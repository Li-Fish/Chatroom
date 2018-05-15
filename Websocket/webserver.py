from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return open('Index.html').read()


app.run('127.0.0.1', 20000)
