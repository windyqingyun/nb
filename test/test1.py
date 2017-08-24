from flask import Flask

app = Flask(__name__)

@app.route('/<name>')
def index(name):
    return name


app.run(host="0.0.0.0",port="8080")
