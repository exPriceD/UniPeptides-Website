from flask import Flask, render_template, request, send_from_directory, g, redirect, jsonify, session
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import run_script
import completion
import os
import json
import datetime

ALLOWED_EXTENSIONS = {'txt'}
SECRET_KEY = '2K4idssi39#skqcmxm1121sak149a9'

app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app=app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'

dbase = None
db = SQLAlchemy(app)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<users {self.id}>"


class SearchResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.String)
    file = db.Column(db.LargeBinary)
    proteins = db.Column(db.String)
    peptides = db.Column(db.String)

    def __repr__(self):
        return f"<search results {self.id}>"


class DatabaseReqests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    date = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    username = db.Column(db.String)
    email = db.Column(db.String)
    sequence = db.Column(db.String)
    scientific_name = db.Column(db.String)
    common_name = db.Column(db.String)
    activity = db.Column(db.String)
    protein_source = db.Column(db.String)
    massDa = db.Column(db.String)
    tissue_source = db.Column(db.String)
    pmid = db.Column(db.String)
    reference = db.Column(db.String)

    def __repr__(self):
        return f"<request {self.id}>"


admin = Admin(app, name="Admin panel", template_mode="bootstrap4")
admin.add_view(ModelView(Users, db.session, name="Users"))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()


@app.route('/database', methods=['GET', 'POST'])
def database():
    return render_template("db.html")


@app.route('/api/database')
def get_db_json():
    with open('templates/peptides_database.json', "r") as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/panel')
def panel():
    user_requests = DatabaseReqests.query.order_by(DatabaseReqests.status).all()
    user_requests = reversed(user_requests)
    return render_template('panel.html', user_requests=user_requests)


@app.route('/panel/add_peptide', methods=["POST", "GET"])
def add_peptide():
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            update_database(form=form, action="add")
    return ''


@app.route('/panel/remove_peptide', methods=["POST", "GET"])
def remove_peptide():
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            update_database(form=form, action="remove")
    return ''


@app.route('/panel/accept', methods=["POST", "GET"])
def accept_request():
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            user_request = DatabaseReqests.query.filter_by(id=int(form["id"])).first()
            user_request.status = "Accepted"
            user_request.sequence = form["sequence"]
            user_request.scientific_name = form["scientific_name"]
            user_request.common_name = form["common_name"]
            user_request.activity = form["activity"]
            user_request.protein_source = form["protein_source"]
            user_request.massDa = form["massDa"]
            user_request.tissue_source = form["tissue_source"]
            user_request.pmid = form["pmid"]
            user_request.reference = form["reference"]
            db.session.commit()
            update_database(form=form, action="add")
            print(f'Request id={int(form["id"])} ACCEPTED')
    return ''


@app.route('/panel/cancel', methods=["POST", "GET"])
def cancel_request():
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            user_request = DatabaseReqests.query.filter_by(id=int(form["id"])).first()
            user_request.status = "Canceled"
            db.session.commit()
            print(f'Request id={int(form["id"])} CANCELED')
    return ''


@app.route('/databaseForm', methods=['POST', 'GET'])
@login_required
def database_form():
    if request.method == "POST":
        form = request.form.to_dict()
        print(form)
        if form:
            sequence = request.form["sequence"]
            scientific_name = form["scientific_name"] if form["scientific_name"] else "not data"
            common_name = form["common_name"] if form["common_name"] else "not data"
            activity = form["activity"] if form["activity"] else "not data"
            protein_source = form["protein_source"] if form["protein_source"] else "not data"
            massDa = form["massDa"] if form["massDa"] else "not data"
            tissue_source = form["tissue_source"] if form["tissue_source"] else "not data"
            pmid = form["pmid"] if form["pmid"] else "not data"
            reference = form["reference"]
            user_email = current_user.email
            user_id = current_user.id
            username = current_user.username
            date = str(datetime.datetime.now()).split('.')[0]
            user_request = DatabaseReqests(
                status="Сonsideration",
                date=date,
                user_id=user_id,
                username=username,
                email=user_email,
                sequence=sequence,
                scientific_name=scientific_name,
                common_name=common_name,
                activity=activity,
                protein_source=protein_source,
                massDa=massDa,
                tissue_source=tissue_source,
                pmid=pmid,
                reference=reference
            )
            db.session.add(user_request)
            db.session.flush()
            db.session.commit()
            print("Запрос добавлен")
    return render_template('form.html')


@app.route('/')
def menu():
    return render_template("menu.html")


@app.route('/account')
@login_required
def account():
    result = SearchResults.query.filter_by(user_id=current_user.id).all()
    requests = DatabaseReqests.query.filter_by(user_id=current_user.id).all()
    if result:
        result = list(reversed(result))
    if requests:
        requests = list(reversed(requests))
    return render_template("account.html", username=current_user.username, results=result, requests=requests)


@app.route('/account/<result_id>')
@login_required
def get_result(result_id):
    result = SearchResults.query.filter_by(id=result_id).first()
    file = result.file
    result_date = result.date
    result_date = result_date.replace(' ', '').replace(':', '')
    if len(file) > 0:
        _file = open(f"uploads/outputs/{result_date}.zip", 'wb')
        _file.write(file)
        _file.close()
    full_path = f"{os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])}\outputs"
    return send_from_directory(full_path, f"{result_date}.zip")


@socketio.on('delete result')
def remove_result(result_id):
    SearchResults.query.filter_by(id=int(result_id['data'])).delete()
    db.session.commit()


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/account")
    if request.method == "POST":
        if "@" in request.form["login"]:
            user = Users.query.filter_by(email=request.form["login"]).first()
        else:
            user = Users.query.filter_by(username=request.form["login"]).first()
            print(user)
        if not user:
            not_user()
        else:
            remember = True if request.form.get('rememberme') else False
            if check_password_hash(pwhash=user.password, password=request.form["password"]):
                login_user(user, remember=remember)
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
            user = Users(username=request.form["username"], email=request.form["email"], password=hash)
            check_status = check_users(username=request.form["username"],email=request.form["email"])
            if check_status == 'ok':
                print(f"{form_data['username']} зарегистрирован!")
                db.session.add(user)
                db.session.flush()
                db.session.commit()
                login_user(Users.query.filter_by(email=request.form["email"]).first())
                session_was_created()
            elif check_status == 'username':
                username_already_exist()
            else:
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
                    result = SearchResults(
                        user_id=current_user.id,
                        date=dt_now,
                        file=blob_file,
                        proteins=proteins,
                        peptides=peptides
                    )
                    db.session.add(result)
                    db.session.flush()
                    db.session.commit()
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
def send_peptides(peptides):
    emit("peptides form db", peptides, namespace='/', broadcast=True)


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


def check_users(email, username):
    if Users.query.filter_by(email=email).all():
        return "email"
    if Users.query.filter_by(username=username).all():
        return "username"
    return "ok"


def update_database(form: dict, action: str):
    with open("templates/peptides_database.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    if action == "add":
        peptides_info = {
            "id": len(json_data["data"]) + 1,
            "sequence": form["sequence"],
            "length": len(form["sequence"]),
            "massDa": form["massDa"] if form["massDa"] else "Not data",
            "scientificName": form["scientific_name"] if form["scientific_name"] else "Not data",
            "commonName": form["common_name"] if form["common_name"] else "Not data",
            "tissueSource": form["tissue_source"] if form["tissue_source"] else "Not data",
            "proteinSource": form["protein_source"] if form["protein_source"] else "Not data",
            "antioxidant": "Yes",
            "antihypertension": "No",
            "antidiabetic": "No",
            "pmid": form["pmid"] if form["pmid"] else "Not data",
            "reference": form["reference"]
        }
        json_data["data"].append(peptides_info)
    else:
        sequence = form["sequence"]
        activity = form["activity"]
        for peptide in json_data["data"]:
            if peptide["sequence"] == sequence and peptide["antioxidant"] == "Yes":
            #if peptide["sequence"] == sequence and peptide["activity"] == activity:
                json_data["data"].remove(peptide)

    with open("templates/peptides_database.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)
    print("Database was updated")


if __name__ == "__main__":
    app.debug = True
    socketio.run(app, allow_unsafe_werkzeug=True)
    with app.app_context():
        db.create_all()
