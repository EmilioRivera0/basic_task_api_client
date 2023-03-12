"""-----------------------------------------------------------------------------------------------------------------------------------
  - Software Name: Task Manager Web Page
  - Language: Python
  - Developer: Emilio Rivera Macías
  - Date: March 10, 2023
  - Contact: emilioriveramacias@gmail.com
  -----------------------------------------------------------------------------------------------------------------------------------"""

#necessary imports ----->
from flask import Flask, render_template, request, redirect, abort
from requests import get, post

#object declaration ----->
#creating the Flask app object 
app = Flask(__name__)
#URL of the Server API (uploaded by me)
# *if this link does not work, clone the "basic task api" repository from my account and upload it to a server to use it instead
SERVER_URL = 'https://task-management-api-0ds8.onrender.com/api/'

#for debugging 
#SERVER_URL = 'http://127.0.0.1:5001/api/'

#function declaration ----->
#home page of task manager with get and post methods to view the tasks and append new ones respectively
@app.route('/', methods=['GET','POST'])
def home():
    """ index page of Task Manager Web Page """
    #complete tasks dictionary
    complete_tasks = {}
    #incomplete tasks dictionary
    incomplete_tasks = {}
    #GET request
    if request.method == 'GET':
        #API server returns a dictionary with an element 'tasks' that contains a list of dictionaries for each task
        try:
            tasks = get(SERVER_URL+'tasks').json()
        except:
            #generate a 500 HTTP error code since it is a problem with the server
            abort(500)
        #iterate through each task to separate them in completed and uncompleted tasks
        #id key-value is removed from the dictionary since it is redundant with the key of the completed and uncompleted tasks dictionaries
        for task in tasks['tasks']:
            if task['estado']:
                complete_tasks[task['id']] = task
                complete_tasks[task['id']].pop('id')
            elif not task['estado']:
                incomplete_tasks[task['id']] = task
                incomplete_tasks[task['id']].pop('id')
        #render home page and return it to the client
        #pass complete and incomplete tasks and its respective dictionary sizes to render in the HTML 
        return render_template('index.html', content={'complete_tasks':complete_tasks,'incomplete_tasks':incomplete_tasks},uncompleted_len=len(incomplete_tasks),completed_len=len(complete_tasks))
    #POST request to append new task
    else:
        #API server returns a dictionary with an element 'tasks' that contains a list of dictionaries for each task including the one recently appended
        post_data = {'name':request.form.get('name')} 
        try:
            tasks = post(SERVER_URL+'append',data=post_data).json()
        except:
            #generate a 500 HTTP error code since it is a problem with the server
            abort(500)
        #iterate through each task to separate them in completed and uncompleted tasks
        #id key-value is removed from the dictionary since it is redundant with the key of the completed and uncompleted tasks dictionaries
        for task in tasks['tasks']:
            if task['estado']:
                complete_tasks[task['id']] = task
                complete_tasks[task['id']].pop('id')
            elif not task['estado']:
                incomplete_tasks[task['id']] = task
                incomplete_tasks[task['id']].pop('id')
        #render home page and return it to the client
        #pass complete and incomplete tasks and its respective dictionary sizes to render in the HTML 
        return render_template('index.html', content={'complete_tasks':complete_tasks,'incomplete_tasks':incomplete_tasks},uncompleted_len=len(incomplete_tasks),completed_len=len(complete_tasks))

#API program start point ----->
if __name__ == '__main__':
    app.run(debug=True)
