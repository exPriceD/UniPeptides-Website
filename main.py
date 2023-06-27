from flask import Flask, render_template, request, send_from_directory, g, redirect, jsonify
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from FDataBase import FDataBase
from UserLogin import UserLogin
from forms import LoginForm
import sqlite3
import run_script
import completion
import os
import json
import datetime


ALLOWED_EXTENSIONS = {'txt'}
DATABASE = 'tmp/users.db'
SECRET_KEY = '2K4idssi39#skqcmxm1121sak149a9'

app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app=app)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'users.db')))
app.config['UPLOAD_FOLDER'] = 'uploads'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

dbase = None


@app.before_request
def before_request():
    global dbase
    db = connect_db()
    dbase = FDataBase(db)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id=user_id, db=dbase)


def connect_db():
    connection = sqlite3.connect(app.config['DATABASE'], check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_connection_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_connection_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route('/database')
def database():
    return render_template("db.html")


@app.route('/api/database')
def get_db_json():
    with open('templates/peptides_database.json', "r") as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/databaseForm')
@login_required
def database_form():
    return render_template('form.html')


@app.route('/')
def menu():
    return render_template("menu.html")


@app.route('/account')
@login_required
def account():
    res = dbase.getSearchResult(current_user.get_username(), current_user.get_email())
    if res:
        res = list(reversed(res))
    return render_template("account.html", username=current_user.get_username(), results=res)


@app.route('/account/<result>')
@login_required
def get_result(result):
    print(result)
    dbase.getfile(current_user.get_email(), result)
    full_path = f"{os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])}\outputs"
    result = result.replace(' ', '').replace(':', '')
    return send_from_directory(full_path, f"{result}.zip")


@socketio.on('delete result')
def remove_result(message):
    dbase.remove_result(current_user.get_email(), message["data"])


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/account")
    if request.method == "POST":
        if "@" in request.form["login"]:
            user = dbase.getUserByEmail(request.form["login"])
        else:
            user = dbase.getUserByName(request.form["login"])
        if not user:
            not_user()
        else:
            remember = True if request.form.get('rememberme') else False
            if check_password_hash(pwhash=user["password"], password=request.form["password"]):
                userLogin = UserLogin().create(user=user)
                login_user(userLogin, remember=remember)
                session_was_created()
                return redirect(request.args.get("next") or "/account")
            else:
                not_password()
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/register', methods=["POST", "GET"])
def registration():
    if current_user.is_authenticated:
        return redirect("/account")

    if request.method == "POST":
        form_data = request.form.to_dict()
        print(form_data)
        if form_data['username'] and form_data["email"] and form_data["password"]:
            hash = generate_password_hash(password=form_data["password"])
            result, status = dbase.addUser(form_data["username"], form_data["email"], hash)
            if result:
                print(f"{form_data['username']} зарегистрирован!")
                user = dbase.getUserByEmail(request.form["email"])
                userLogin = UserLogin().create(user=user)
                login_user(userLogin)
                session_was_created()
            else:
                print(status)
                if status == 'username':
                    username_already_exist()
                if status == 'email':
                    email_already_exist()
    return render_template("register.html")


@app.route('/search', methods=['POST', 'GET'])
def get_value():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        if 'userProteins' in request.files:
            file = request.files['userProteins']
            file.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}/inputs", "userProteins.txt"))
        if 'userPeptides' in request.files:
            file = request.files['userPeptides']
            file.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}/inputs", "userPeptides.txt"))
        print(form_data)
        if not("userProteins" in form_data.keys()) or len(form_data["proteins_value"]) > 0:
            if not("userPeptides" in form_data.keys()) or len(form_data["peptides_value"]) > 0:
                dt_now = str(datetime.datetime.now()).split('.')[0]
                run_script.run_processing(form_data)
                filename = completion.creating_zip()
                change_css(filename)
                if current_user.is_authenticated:
                    blob_file = convert_to_binary_data(f"uploads/outputs/{filename}.zip")
                    proteins = ','.join(get_proteins())
                    peptides = ','.join(get_peptides())
                    result = dbase.addResult(
                        current_user.get_username(),
                        current_user.get_email(),
                        dt_now,
                        blob_file,
                        proteins,
                        peptides
                    )
                    if result:
                        print('Файл добавлен')
                completion.remove_config()

    return render_template("search.html", loading_atr="flex", end_atr="none")


@app.route('/uploads/outputs/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    filename = filename.replace('.zip', '')
    full_path = f"{os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])}\outputs"

    return send_from_directory(full_path, f"{filename}.zip")


@socketio.event
def change_css(filename):
    emit('my response', filename, namespace='/', broadcast=True)


@socketio.event
def username_already_exist():
    emit('username already exist', namespace='/', broadcast=True)


@socketio.event
def email_already_exist():
    emit('email already exist', namespace='/', broadcast=True)


@socketio.event
def session_was_created():
    emit('session was created', namespace='/', broadcast=True)


@socketio.event
def result_was_deleted():
    emit('result was deleted', namespace='/', broadcast=True)


@socketio.event
def not_user():
    emit('user not found', namespace='/', broadcast=True)


@socketio.event
def not_password():
    emit('incorrect password', namespace='/', broadcast=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def convert_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)


def get_proteins():
    with open("config.json", "r") as json_cfg:
        config = json.load(json_cfg)
    return config["proteins"]["value"]


def get_peptides():
    with open("config.json", "r") as json_cfg:
        config = json.load(json_cfg)
    return config["peptides"]["value"]


if __name__ == "__main__":
    app.debug = True
    socketio.run(app, allow_unsafe_werkzeug=True)
