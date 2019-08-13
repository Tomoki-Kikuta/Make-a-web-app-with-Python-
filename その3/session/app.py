from flask import  Flask, session

app = Flask(__name__)

app.secret_key = 'wj9jr2jg@249j0J4h20JaV91A03f4j2'

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in'] == True:
        return "you are logged in"
    else:
        session["logged_in"] = True
        return "you are not logged in" 