from flask import Flask, render_template, url_for, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import run_script
import completion
import os

app = Flask(__name__)
socketio = SocketIO(app=app)


@app.route('/')
def index():
    return render_template("index.html", loading_atr="flex", end_atr="none")


@app.route('/', methods=['POST', 'GET'])
def get_value():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        print(form_data)
        run_script.run_processing(form_data)
        filename = completion.creating_zip()
        #completion.remove_user_config()
        change_css(filename)

    return render_template("index.html", loading_atr="none", end_atr="flex")


app.config['UPLOAD_FOLDER'] = 'output'

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    print(app.root_path)
    full_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print(full_path)
    print(filename)
    return send_from_directory(full_path, filename)

@socketio.event
def change_css(filename):
    emit('my response', filename, namespace='/', broadcast=True)


if __name__ == "__main__":
    app.debug = True
    socketio.run(app, allow_unsafe_werkzeug=True)