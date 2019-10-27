from flask import request, Response, abort, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from collections import defaultdict
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from datetime import datetime
from application import app, db
from application.models import User


login_manager = LoginManager()
login_manager.init_app(app)
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

@app.route('/')
def to_home():
    return redirect(url_for("home"))


@app.route("/home/")
def home():
    return render_template("home.html")

@app.route('/register/', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        # ログイン用ユーザー作成
        return render_template("new_register.html")
    else:
        if request.form['username'] and request.form['password'] and request.form['id']:
            newUser = User(id=request.form['id'], username=request.form['username'], password=request.form["password"])
            db.session.add(newUser)
            db.session.commit()
            return render_template('result.html', username=request.form['username'])
        else:
            return render_template('error.html')


@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # ユーザーチェックをする
        users = User.query.all()
        for user in users:
            # TODO: databaseから効率的に取得する方が良い
            if user.username == request.form["username"] and user.password == request.form["password"]:
                # ユーザーが存在した場合はログイン
                login_user(user)
                return redirect(url_for("protected", user=user.username))
        return render_template("error.html")
    else:
        return render_template("login.html")


# ログアウトパス
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return render_template("logout.html")


# ログインしないと表示されないパス
@app.route('/protected/<user>/')
@login_required
def protected(user):
    return render_template("form.html", username=user)


