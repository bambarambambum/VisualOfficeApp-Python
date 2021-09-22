from os import environ
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from prometheus_flask_exporter import PrometheusMetrics
# Тест, убрать
from flask_cors import CORS
from pathlib import Path

script_path = Path(__file__).absolute().parent

# Configuration
DATABASE_USER = environ.get('DATABASE_USER')
if (DATABASE_USER is None):
    DATABASE_USER = "admin"
DATABASE_PASSWORD = environ.get('DATABASE_PASSWORD')
if (DATABASE_PASSWORD is None):
    DATABASE_PASSWORD = "admin"
DATABASE_DB = environ.get('DATABASE_DB')
if (DATABASE_DB is None):
    DATABASE_DB = "visualoffice"
DATABASE_HOST = environ.get('DATABASE_HOST')
if (DATABASE_HOST is None):
    DATABASE_HOST = "localhost"

app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app, group_by='endpoint')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_DB}'
db = SQLAlchemy(app)


@dataclass
class Manager(db.Model):
    id: int
    name: str
    position: str
    age: int
    email: str
    n_subordinate: int
    users: object
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    position = db.Column(db.String(80))
    age = db.Column(db.Integer)
    email = db.Column(db.String(40))
    n_subordinate = db.Column(db.Integer)
    users = db.relationship('User', backref='managers')


@dataclass
class User(db.Model):
    id: int
    name: str
    position: str
    age: int
    email: str
    manager_id: int
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    position = db.Column(db.String(80))
    age = db.Column(db.Integer)
    email = db.Column(db.String(40))
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))


@app.route('/api/managers')
def managers():
    managers = []
    try:
        managers = Manager.query.all()
    except:
        print("Ошибка чтения из БД")
    return jsonify(managers)


@app.route('/api/managers/<int:id>')
@metrics.counter(
    'invocation_by_manager', 'Number of invocations by manager', labels={
        'collection': lambda: request.view_args['id'],
        'status': lambda resp: resp.status_code
    })
def get_manager(id):
    manager = ""
    try:
        manager = Manager.query.get(id)
    except:
        print("Ошибка чтения из БД")
    return jsonify(manager)


@app.route('/api/managers/<int:id>/users')
def get_manager_users(id):
    manager = ""
    try:
        manager = Manager.query.get(id)
    except:
        print("Ошибка чтения из БД")
    return jsonify(manager.users)


@app.route('/api/managers/<int:id>/users/<int:user_id>')
@metrics.counter(
    'invocation_by_user', 'Number of invocations by user', labels={
        'collection': lambda: request.view_args['user_id'],
        'status': lambda resp: resp.status_code
    })
def get_manager_user(id, user_id):
    manager = ""
    user = ""
    try:
        manager = Manager.query.get(id)
        for u in manager.users:
            if u.id == user_id:
                user = u
    except:
        print("Ошибка чтения из БД")
    return jsonify(user)


@app.route('/api/managers/users')
def manager_users():
    users = []
    try:
        users = User.query.all()
    except:
        print("Ошибка чтения из БД")
    return jsonify(users)


@app.route('/api/users')
def users():
    users = []
    try:
        users = User.query.all()
    except:
        print("Ошибка чтения из БД")
    return jsonify(users)


@app.route('/api/users/<int:id>')
def get_user(id):
    user = ""
    try:
        user = User.query.get(id)
    except:
        print("Ошибка чтения из БД")
    return jsonify(user)


if __name__ == '__main__':
   app.run()
