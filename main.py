from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit
import run_script
import completion
import os
#Соседняя аминокислота с С-конца
app = Flask(__name__)
socketio = SocketIO(app=app)
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}


@app.route('/')
def index():
    return render_template("search.html", loading_atr="flex", end_atr="none")


@app.route('/database')
def database():
    return render_template("database.html", loading_atr="flex", end_atr="none")


@app.route('/', methods=['POST', 'GET'])
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
                run_script.run_processing(form_data)
                filename = completion.creating_zip()
                completion.remove_config()
                change_css(filename)

    return render_template("search.html", loading_atr="none", end_atr="flex")


@app.route('/uploads/outputs/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    filename = filename.replace('.zip', '')
    full_path = f"{os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])}\outputs"

    return send_from_directory(full_path, f"{filename}.zip")


@socketio.event
def change_css(filename):
    emit('my response', filename, namespace='/', broadcast=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.debug = True
    socketio.run(app, allow_unsafe_werkzeug=True)