from flask import Flask, render_template, request, send_from_directory, redirect, jsonify, flash
#from flask_socketio import SocketIO, emit
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
import shutil


ALLOWED_EXTENSIONS = {'txt'}
SECRET_KEY = os.urandom(24)

application = Flask(__name__)
application.config.from_object(__name__)
#socketio = SocketIO(app=application)

application.config['UPLOAD_FOLDER'] = 'uploads'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(application)
login_manager.login_view = 'login'

dbase = None
db = SQLAlchemy(application)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String, nullable=True)
    role = db.Column(db.String)

    def __init__(self, username, email, password, role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def get_role(self):
        return self.role

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


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()


admin = Admin(application, name="Admin panel", template_mode="bootstrap4")
admin.add_view(ModelView(Users, db.session, name="Users"))


@application.route('/admin')
def admin():
    if current_user.role != "Admin":
        return 'You dont have enough rights to view this page'


@application.route('/database', methods=['GET', 'POST'])
def database():
    return render_template("db.html")


@application.route('/api/database')
def get_db_json():
    with open('peptides_database/peptides.json', "r") as f:
        data = json.load(f)
    return jsonify(data)


@application.route('/panel')
def panel():
    try:
        if current_user.role == "User":
            return 'You dont have enough rights to view this page'
    except AttributeError:
        return redirect('/login')
    user_requests = DatabaseReqests.query.order_by(DatabaseReqests.status).all()
    user_requests = reversed(user_requests)
    return render_template('panel.html', user_requests=user_requests)


@application.route('/panel/add_peptide', methods=["POST", "GET"])
def add_peptide():
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            update_database(form=form, action="add")
    return ''


@application.route('/panel/remove_peptide', methods=["POST", "GET"])
def remove_peptide():
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            update_database(form=form, action="remove")
    return ''


@application.route('/panel/accept', methods=["POST", "GET"])
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


@application.route('/panel/cancel', methods=["POST", "GET"])
def cancel_request():
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            user_request = DatabaseReqests.query.filter_by(id=int(form["id"])).first()
            user_request.status = "Canceled"
            db.session.commit()
            print(f'Request id={int(form["id"])} CANCELED')
    return ''


@application.route('/panel/edit_peptide', methods=["POST", "GET"])
def edit_peptide():
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            update_database(form=form, action="edit")
    return ''


@application.route('/database/form', methods=['POST', 'GET'])
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


@application.route('/')
def menu():
    return render_template("menu.html")


@application.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    result = SearchResults.query.filter_by(user_id=current_user.id).all()
    requests = DatabaseReqests.query.filter_by(user_id=current_user.id).all()
    if result:
        result = list(reversed(result))
    if requests:
        requests = list(reversed(requests))
    return render_template("account.html", username=current_user.username, results=result, requests=requests)


@application.route('/account/<result_id>')
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
    full_path = f"{os.path.join(application.root_path, application.config['UPLOAD_FOLDER'])}\outputs"
    return send_from_directory(full_path, f"{result_date}.zip")


@application.route('/account/download', methods=["POST", "GET"])
def download_selected():
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            get_blob(form=form)
    return send_from_directory('uploads\outputs', f"selectedResults.zip")


@application.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/account")
    if request.method == "POST":
        if "@" in request.form["login"]:
            user = Users.query.filter_by(email=request.form["login"]).first()
        else:
            user = Users.query.filter_by(username=request.form["login"]).first()
        if not user:
            return jsonify({'status': 'User not found!'})
        else:
            remember = True if request.form["rememberme"] == 'true' else False
            if check_password_hash(pwhash=user.password, password=request.form["password"]):
                login_user(user, remember=remember)
                return jsonify({'status': 'Success!'})
            else:
                return jsonify({'status': 'Incorrect password!'})
    return render_template("login.html")


@application.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@application.route('/register', methods=["POST", "GET"])
def registration():
    if current_user.is_authenticated:
        return redirect("/account")
    if request.method == "POST":
        form_data = request.form.to_dict()
        print(form_data)
        if form_data['username'] and form_data["email"] and form_data["password"]:
            hash = generate_password_hash(password=form_data["password"])
            user = Users(username=request.form["username"], email=request.form["email"], password=hash, role="User")
            check_status = check_users(username=request.form["username"],email=request.form["email"])
            if check_status == 'ok':
                print(f"{form_data['username']} зарегистрирован!")
                db.session.add(user)
                db.session.flush()
                db.session.commit()
                login_user(Users.query.filter_by(email=request.form["email"]).first())
                return jsonify({'status': 'Success!'})
            elif check_status == 'username':
                return jsonify({'status': 'Username already exist!'})
            else:
                return jsonify({'status': 'Email already exist!'})
    return render_template("register.html")


@application.route('/search', methods=['POST', 'GET'])
def get_value():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        if 'userProteins' in request.files:
            file = request.files['userProteins']
            file.save(os.path.join(f"{application.config['UPLOAD_FOLDER']}/inputs", "userProteins.txt"))
        if 'userPeptides' in request.files:
            file = request.files['userPeptides']
            file.save(os.path.join(f"{application.config['UPLOAD_FOLDER']}/inputs", "userPeptides.txt"))
        print(form_data)
        if not("userProteins" in form_data.keys()) or len(form_data["proteins_value"]) > 0:
            if not("userPeptides" in form_data.keys()) or len(form_data["peptides_value"]) > 0:
                dt_now = str(datetime.datetime.now()).split('.')[0]
                run_script.run_processing(form_data)
                filename = completion.creating_zip()
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
                return jsonify({"filename": f"{filename}.zip"})

    return render_template("search.html", loading_atr="flex", end_atr="none")


@application.route('/account/remove', methods=['POST', 'GET'])
def remove_result():
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            SearchResults.query.filter_by(id=int(form["id"])).delete()
            db.session.commit()
    return ''


@application.route('/uploads/outputs/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    full_path = f"{os.path.join(application.root_path, application.config['UPLOAD_FOLDER'])}\outputs"
    return send_from_directory(full_path, filename)


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
    with open("peptides_database/peptides.json", "r", encoding="utf-8") as f:
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
            "activity": form["activity"],
            "pmid": form["pmid"] if form["pmid"] else "Not data",
            "reference": form["reference"]
        }
        json_data["data"].append(peptides_info)
    elif action == "edit":
        for peptide in json_data["data"]:
            if peptide["sequence"] == form["sequence"] and peptide["activity"] == form["activity"]:
                peptide["massDa"] = form["massDa"]
                peptide["scientificName"] = form["scientific_name"]
                peptide["commonName"] = form["common_name"]
                peptide["tissueSource"] = form["tissue_source"]
                peptide["proteinSource"] = form["protein_source"]
                peptide["pmid"] = form["pmid"]
                peptide["reference"] = form["reference"]
    else:
        sequence = form["sequence"]
        activity = form["activity"]
        for peptide in json_data["data"]:
            if peptide["sequence"] == sequence and peptide["activity"] == activity:
                json_data["data"].remove(peptide)

    with open("peptides_database/peptides.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)
    print("Database was updated")


def get_blob(form: dict):
        blobs = {}
        if not os.path.exists("uploads/outputs/selectedResults"):
            try:
                os.mkdir("uploads/outputs/selectedResults")
            except: '?????????'
        for id in form.keys():
            result = SearchResults.query.filter_by(id=id).first()
            result_date = result.date
            result_date = result_date.replace(' ', '').replace(':', '')
            blobs[result_date] = result.file
        while len(blobs) != len(form):
            pass
        for date in blobs.keys():
            _file = open(f"uploads/outputs/selectedResults/{date}.zip", 'wb')
            _file.write(blobs[date])
            _file.close()
        shutil.make_archive(
            'selectedResults',
            'zip',
            f"uploads/outputs/selectedResults"
        )
        shutil.move(f"selectedResults.zip", "uploads/outputs\\")


if __name__ == "__main__":
    application.debug = True
    #socketio.run(application, allow_unsafe_werkzeug=True, host='0.0.0.0')
    application.run()
    with application.app_context():
        db.create_all()
