from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import configparser

config = configparser.ConfigParser()
config.read("config")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:admin@localhost/visualoffice'
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
    app.run(port=5001)