from flask import Flask, request, Response, abort, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/testdb"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    # def __repr__(self):
    #     return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return user.get(user_id)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register/', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        # ログイン用ユーザー作成
        return render_template("new_register.html")
    else:
        if request.form['username'] and request.form['password']:
            newUser = User(username=request.form['username'], password=request.form["password"])
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
            if user.username == request.form["username"] and user.password == request.form["password"]:
                # ユーザーが存在した場合はログイン
                login_user(user.id, users)
                return render_template("form.html")
        return render_template("error.html")
    else:
        return render_template("login.html")


# ログアウトパス
@app.route('/logout/')
@login_required
def logout(user):
    logout_user(user.id, user)
    return render_template("logout.html")


# ログインしないと表示されないパス
@app.route('/protected/')
@login_required
def protected():
    return render_template("form.html")


@app.cli.command('initdb')
def initdb_command():
    db.create_all()