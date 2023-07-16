from flask import render_template, request, send_from_directory, redirect, jsonify
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import run_script
import completion
import os
import json
import datetime
from threading import Thread
import shutil
import secrets

from config import application, mail, login_manager
from models import db, Users, SearchResults, DatabaseReqests

ALLOWED_EXTENSIONS = {'txt'}


@application.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()


@application.route('/404')
def error():
    return render_template('errors.html')


@application.route('/database', methods=['GET', 'POST'])
def database():
    auth = False
    if current_user.is_authenticated and current_user.role != 'User':
        auth = True
    return render_template("peptides_db.html", is_auth=auth)


@application.route('/api/database')
def get_db_json():
    with open('peptides_database/peptides.json', "r") as f:
        data = json.load(f)
    return jsonify(data)


@application.route('/panel')
@login_required
def panel():
    try:
        if current_user.role == "User":
            return 'You dont have enough rights to view this page'
    except AttributeError:
        return redirect('/login')
    auth = False
    if current_user.is_authenticated and current_user.role != 'User':
        auth = True
    user_requests = DatabaseReqests.query.order_by(DatabaseReqests.status).all()
    user_requests = reversed(user_requests)
    return render_template('panel.html', user_requests=user_requests, is_auth=auth)


@application.route('/panel/add_peptide', methods=["POST", "GET"])
@login_required
def add_peptide():
    try:
        if current_user.role == "User":
            return 'You dont have enough rights to view this page'
    except AttributeError:
        return redirect('/login')
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            update_database(form=form, action="add")
    return ''


@application.route('/panel/remove_peptide', methods=["POST", "GET"])
def remove_peptide():
    try:
        if current_user.role == "User":
            return 'You dont have enough rights to view this page'
    except AttributeError:
        return redirect('/login')
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            update_database(form=form, action="remove")
    return ''


@application.route('/panel/accept', methods=["POST", "GET"])
@login_required
def accept_request():
    try:
        if current_user.role == "User":
            return 'You dont have enough rights to view this page'
    except AttributeError:
        return redirect('/login')
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
@login_required
def cancel_request():
    try:
        if current_user.role == "User":
            return 'You dont have enough rights to view this page'
    except AttributeError:
        return redirect('/login')
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            user_request = DatabaseReqests.query.filter_by(id=int(form["id"])).first()
            user_request.status = "Canceled"
            db.session.commit()
            print(f'Request id={int(form["id"])} CANCELED')
    return ''


@application.route('/panel/edit_peptide', methods=["POST", "GET"])
@login_required
def edit_peptide():
    try:
        if current_user.role == "User":
            return 'You dont have enough rights to view this page'
    except AttributeError:
        return redirect('/login')
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
    auth = False
    if current_user.is_authenticated and current_user.role != 'User':
        auth = True
    return render_template("menu.html", is_auth=auth)


@application.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    auth = False
    if current_user.role != 'User':
        auth = True
    result = SearchResults.query.filter_by(user_id=current_user.id).all()
    requests = DatabaseReqests.query.filter_by(user_id=current_user.id).all()
    if result:
        result = list(reversed(result))
    if requests:
        requests = list(reversed(requests))
    return render_template("account.html", username=current_user.username, results=result, requests=requests, is_auth=auth)


@application.route('/account/<result_id>')
@login_required
def get_result(result_id):
    try:
        result = SearchResults.query.filter_by(id=result_id).first()
        if not (result):
            return "<h1>Result not found <b>support@unipeptides.ru</b></h1>"
    except:
        return '<h1>Unknown error </h1><b>support@unipeptides.ru</b>'
    if int(result.user_id) != int(current_user.id):
        return "<h1>You don't have enough rights to download this result <b>support@unipeptides.ru</b></h1>"
    file = result.file
    result_date = result.date
    result_date = result_date.replace(' ', '').replace(':', '')
    if len(file) > 0:
        _file = open(f"uploads/outputs/{result_date}.zip", 'wb')
        _file.write(file)
        _file.close()
        full_path = f"{os.path.join(application.root_path, application.config['UPLOAD_FOLDER'])}/outputs"
        return send_from_directory(full_path, f"{result_date}.zip")
    return f'<h1>Result from {result_date} not found. If you think this is a mistake, write to us by email <b>support@unipeptides.ru</b> </h1>'


@application.route('/account/download', methods=["POST", "GET"])
def download_selected():
    if request.method == "POST":
        form = request.form.to_dict()
        if form:
            get_blob(form=form)
    return send_from_directory('uploads/outputs', f"selectedResults.zip")


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
                print(remember)
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
            user = Users(username=request.form["username"], email=request.form["email"], password=hash, role="User",
                         token='', token_date=None)
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


@application.route('/password_recovery', methods=['POST', 'GET'])
def password_recovery():
    if request.method == 'POST':
        form = request.form.to_dict()
        print(form)
        if form:
            token = secrets.token_hex(24)
            print(token)
            user = Users.query.filter_by(email=form["email"]).first()
            if not(user):
                return jsonify({'status': 'Failed'})
            user.token = token
            user.token_date = datetime.datetime.today()
            db.session.commit()
            body = f"Your link for reset password: http://127.0.0.1:5000/password_recovery/{token}"
            send_mail(subject="Reset password", recipient=form["email"], body=body)
            return jsonify({'status': 'Success'})
    return render_template('password_recovery_email.html')


@application.route('/password_recovery/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if request.method == 'GET':
        user = Users.query.filter_by(token=token).first()
        if not(user):
            return render_template('password_recovery_pass.html', token='error')
        if (datetime.datetime.today() - user.token_date).total_seconds() > 600:
            return render_template('password_recovery_pass.html', token='error')
    if request.method == 'POST':
        form = request.form.to_dict()
        user = Users.query.filter_by(token=token).first()
        if form and user:
            hash = generate_password_hash(password=form["pass1"])
            user.password = hash
            user.token = None
            user.token_date = None
            db.session.commit()
            print('Password changed')
            return jsonify({'status': 'Success'})
        print('Failed')
        return jsonify({'status': 'Failed'})
    return render_template('password_recovery_pass.html', token='success')


@application.route('/search', methods=['POST', 'GET'])
def get_value():
    auth = False
    if current_user.is_authenticated and current_user.role != 'User':
        auth = True
    if request.method == 'POST':
        form_data = request.form.to_dict()
        if 'userProteins' in request.files:
            file = request.files['userProteins']
            file.save(os.path.join(f"{application.config['UPLOAD_FOLDER']}/inputs", "userProteins.txt"))
            print(file)
        if 'userPeptides' in request.files:
            file = request.files['userPeptides']
            file.save(os.path.join(f"{application.config['UPLOAD_FOLDER']}/inputs", "userPeptides.txt"))
        print(form_data)
        if not("userProteins" in form_data.keys()) or len(form_data["proteins_value"]) > 0:
            if not("userPeptides" in form_data.keys()) or len(form_data["peptides_value"]) > 0:
                dt_now = str(datetime.datetime.now()).split('.')[0]
                missing = run_script.run_processing(form_data)
                filename = completion.creating_zip()
                while not (os.path.exists(f"{os.getcwd()}/uploads/outputs/{filename}.zip")):
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
                message_title = ''
                message = ''
                if missing:
                    message_title = 'Proteins not found:'
                    message = ', '.join(missing)
                return jsonify(
                    {
                        'filename': f'{filename}.zip',
                        'message_title': message_title,
                        'message': message
                    }
                )

    return render_template("search.html", loading_atr="flex", end_atr="none", is_auth=auth)


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


def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject: str, recipient: str, body: str, **kwargs):
    msg = Message(subject, sender=application.config['MAIL_DEFAULT_SENDER'], recipients=[recipient])
    #msg.html = render_template(template,  **kwargs)
    msg.body = body
    thr = Thread(target=async_send_mail,  args=[application,  msg])
    thr.start()
    return thr


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
        shutil.move(f"selectedResults.zip", "uploads/outputs/")


if __name__ == "__main__":
    application.debug = True
    application.run()
    with application.app_context():
        db.create_all()
