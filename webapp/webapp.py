from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)

BASE = "http://localhost:5001"

@app.route('/')
def main():
    managers = ''
    url = BASE + "/api/users"
    try:
        managers = json.loads(requests.get(BASE + "/api/managers").text)
    except:
        print("Ошибка чтения из БД")
    return render_template('index.html', title = "Главная", managers = managers, url = url)

@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    user = ''
    manager = ''
    try:
        user = json.loads(requests.get(BASE + "/api/users/" + str(id)).text)
        manager = json.loads(requests.get(BASE + "/api/managers/" + str(user["manager_id"])).text)
    except:
        print("Ошибка чтения из БД")
    return render_template('edit.html', title = "Редактировать", user = user, manager = manager)

@app.route('/edit/<int:id>', methods=['PUT','POST'])
def save(id):
    user = ''
    manager = ''
    #try:
    user = request.form.to_dict()
    manager = json.loads(requests.get(BASE + "/api/managers/" + str(user["manager_id"])).text)
    #except:
    #print("Ошибка чтения из БД")
    return render_template('edit.html', title = "Редактировать", user = user, manager = manager, success = "Данные успешно сохранены")

if __name__ == '__main__':
    app.run(port=5000)