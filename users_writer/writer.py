from os import environ
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
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


@app.route('/api/users/<int:id>', methods=['POST'])
def put_user(id):
    data = request.values
    if data is not None:
        user = User.query.get(id)
        user.manager_id = data['manager_id']
        user.name = data['name']
        user.position = data['position']
        user.age = data['age']
        user.email = data['email']
    try:
        db.session.commit()
    except:
        print("Ошибка записи в БД")
    return "success"


if __name__ == '__main__':
    app.run()
