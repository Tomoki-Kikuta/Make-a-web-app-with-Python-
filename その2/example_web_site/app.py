from flask import Flask,request,render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/login',methods = ["GET"])
def render_form():
    return render_template("login.html")

@app.route("/login",methods = ["POST"])
def login():
    if request.form["username"] and request.form["email"]:
        return render_template("cheack.html", username=request.form["username"], email=request.form["email"])
    else:
        return render_template("error.html")  

@app.route("/upload", methods = ["GET"])
def upload_form():
    return render_template("upload.html")  
    
@app.route("/upload", methods = ["POST"])
def upload_file():
    if request.form["name"] and request.files["image"]:
        f = request.files["image"]
        filepath= 'static/' + secure_filename(f.filename)
        f.save(filepath)
        return render_template('result.html',name=request.form['name'],image_url=filepath)


