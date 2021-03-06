from os import environ
from flask import Flask, render_template, request
import json
import requests
from prometheus_flask_exporter import PrometheusMetrics

# Configuration
READER_HOST = environ.get('READER_HOST')
if (READER_HOST is None):
    READER_HOST = "localhost"
READER_PORT = environ.get('READER_PORT')
if (READER_PORT is None):
    READER_PORT = "8001"
WRITER_HOST = environ.get('WRITER_HOST')
if (WRITER_HOST is None):
    WRITER_HOST = "localhost"
WRITER_PORT = environ.get('WRITER_PORT')
if (WRITER_PORT is None):
    WRITER_PORT = "8002"

app = Flask(__name__)

BASE = f"http://{READER_HOST}:{READER_PORT}"
metrics = PrometheusMetrics(app, group_by='endpoint')

@app.route('/')
def main():
    managers = ''
    url = BASE + "/api/users"
    try:
        managers = json.loads(requests.get(BASE + "/api/managers").text)
    except:
        print("Ошибка чтения из БД")
    return render_template('index.html', title="Главная", managers=managers, url=url)


@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    user = ''
    manager = ''
    try:
        user = json.loads(requests.get(BASE + "/api/users/" + str(id)).text)
        manager = json.loads(requests.get(BASE + "/api/managers/" + str(user["manager_id"])).text)
    except:
        print("Ошибка чтения из БД")
    return render_template('edit.html', title="Редактировать", user=user, manager=manager)


@app.route('/edit/<int:id>', methods=['PUT', 'POST'])
def save(id):
    user = ''
    manager = ''
    try:
        user = request.form.to_dict()
        manager = json.loads(requests.get(BASE + "/api/managers/" + str(user["manager_id"])).text)
        url = f'http://{WRITER_HOST}:{WRITER_PORT}/api/users/' + user['id']
        requests.post(url, data=user)
    except:
        print("Ошибка чтения из БД")
    return render_template('edit.html', title="Редактировать", user=user, manager=manager, success="Данные успешно сохранены")


if __name__ == '__main__':
    app.run()
