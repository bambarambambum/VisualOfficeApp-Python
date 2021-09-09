from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import configparser
# Тест, убрать
from flask_cors import CORS

config = configparser.ConfigParser()
config.read("config")
app = Flask(__name__)
CORS(app)
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

@app.route('/api/users/<int:id>', methods=['POST'])
def put_user(id):
    user = ""
    try:
        user = User.query.get(id)
    except:
        print("Ошибка чтения из БД")
    return jsonify(user)

if __name__ == '__main__':
    app.run(port=5002)