from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Enikeev-project4-secret-phrase'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enikeev_project4.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/locations/', methods=['GET'])
def locations_list():
    return jsonify([])

@app.route('/events/', methods=['GET'])
def events_list():
    return jsonify([])

@app.route('/enrollments/<int:event_id>', methods=['DELETE', 'POST'])
def enrollments_processing(event_id):
    return jsonify({"status":"success"})

@app.route('/register/', methods=['POST'])
def register_user():
    return jsonify({"status":"ok","id":1})

@app.route('/auth/', methods=['POST'])
def auth_user():
    return jsonify({"status":"success","key":111111111})

@app.route('/profile/', methods=['GET'])
def get_profile():
    return jsonify({"id":1,"picture":"","city":"nsk","about":"", 'enrollments':[]})

@app.errorhandler(404)
def page_not_found(error):
    return 'Такой страницы нет'

if __name__ == '__main__':
    app.run()