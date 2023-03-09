#-----> Necessary imports
from flask import Flask, render_template, request, redirect
from requests import get, post

app = Flask(__name__)
SERVER_URL = 'https://task-management-api-0ds8.onrender.com/api/'

@app.route('/', methods=['GET','POST'])
def home():
    print('se ejecuta home')
    if request.method == 'GET':
        tasks = get(SERVER_URL+'tasks').json()
        print(tasks)
        return render_template('index.html', response=tasks)
    else: #POST
        pass

if __name__ == '__main__':
    app.run(debug=True)
