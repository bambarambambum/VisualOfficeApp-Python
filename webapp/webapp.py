from flask import Flask, render_template
import json
import requests

app = Flask(__name__)

BASE = "http://localhost:5001"

@app.route('/')
def main():
    managers = ''
    try:
        managers = json.loads(requests.get(BASE + "/api/managers").text)
    except:
        print("Ошибка чтения из БД")
    return render_template('index.html', title = "Главная", managers = managers)

if __name__ == '__main__':
    app.run(port=5000)