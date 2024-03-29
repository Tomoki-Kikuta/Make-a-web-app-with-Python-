from flask import Flask, make_response, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    try:
        count = request.cookies.get('count')
        if count != None:
            count = int(count) + 1
        else:
            count = 0
        resp = make_response(render_template('index.html', count=count))
        resp.set_cookie('count', str(count))
        return resp 
    except Exception as e:
        return render_template('error.html'), 500

