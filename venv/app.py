from flask import Flask, request, render_template, redirect, url_for, abort
from werkzeug.utils import secure_filename
from random import random
from datetime import datetime
# from flask import Flask, login_user, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flasknote'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(120), index=True, unique=True)
    user_image_url = db.Column(db.String(120), index=True, unique=False)
    date_published = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    twitter_id = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return '<User%r>' % self.username


class Contents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, unique=True)
    contents = db.Column(db.String(144), index=True, unique=True)
    date_published = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Contents%r>' % self.contents


@app.route('/reply/1', methods=['GET'])
def answerß():
    return render_template('answer.html')


@app.route('/login', methods=['GET'])
def render_form():
    return render_template('login.html')


# @app.route("/login")
@app.route("/login", methods=['POST'])
def login():
    # データベースからidを使用してユーザーのインスタンスを取得
    user = User.query.get(request.form["id"])  # id=request.form["id"])

    if user is None:
        abort(404)
    # このユーザー情報を元にセッションを生成
    login_user(user, True)
    # ユーザ情報ページにリダイレクト
    return render_template('userInfo.html', loginuser=user)


#  return redirect(url_for('index'))

@app.route('/userList', methods=['GET'])
def userList():
    users = User.query.all()
    return render_template('userList.html', users=users)


@login_required
def settings():
    return redirect(url_for('index'))


# 処理を実装する


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/upload', methods=['GET'])
def render_upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.form['name'] and request.files['image']:
        f = request.files['image']
        filepath = 'static/' + secure_filename(f.filename)
        f.save(filepath)
        return render_template('result.html', name=request.form['name'], image_url=filepath)


@app.route('/userform')
def form():
    return render_template('userForm.html')


@app.route('/register', methods=['POST'])
def register():
    if request.form['username'] and request.form['description'] and request.files['image'] and request.form[
        'twitter_id']:

        f = request.files['image']
        filepath = 'static/' + secure_filename(f.filename)
        f.save(filepath)

        filepath = '/' + filepath

        newUser = User(username=request.form['username'],
                       description=request.form['description'],
                       user_image_url=filepath,
                       twitter_id=request.form['twitter_id'])
        db.session.add(newUser)
        db.session.commit()

        return render_template('result.html', username=request.form['username'],
                               description=request.form['description'])
    else:
        return render_template('error.html')


@app.route('/')
def index():
    return render_template('index.html')
