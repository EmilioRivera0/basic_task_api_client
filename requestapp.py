"""-----------------------------------------------------------------------------------------------------------------------------------
  - Software Name: Task Manager Web Page
  - Language: Python
  - Developer: Emilio Rivera Macías
  - Date: March 10, 2023
  - Contact: emilioriveramacias@gmail.com
  -----------------------------------------------------------------------------------------------------------------------------------"""

# *estado = status

#necessary imports ----->
from flask import Flask, render_template, request, abort, redirect
from requests import get, post, put, delete

#object declaration ----->
#creating the Flask app object 
app = Flask(__name__)
#URL of the Server API (uploaded by me)
# *if this link does not work, clone the "basic task api" repository from my account and upload it to a server to use it instead
#SERVER_URL = 'https://task-management-api-0ds8.onrender.com/api/'

#for debugging 
SERVER_URL = 'http://127.0.0.1:5001/api/'

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
        #post data to be sent to the API server
        post_data = {'name':request.form.get('name')} 
        try:
            #API server returns a dictionary with an element 'tasks' that contains a list of dictionaries for each task including the one recently appended
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

#get method to modify the state of the indicated task
@app.route('/update/<int:_id>',methods=['GET'])
def update_status(_id):
    """ update the status of the specified task to completed """
    #put data to be sent to the API serve1r
    put_data = {'id':_id}
    try:
        #try put request on the server to change the status of the specified task
        put(SERVER_URL+'update',data=put_data)
    except:
        #generate 404 error if an exception is thrown
        abort(404)
    #redirect to index page to view changes
    return redirect('/',308)

#delete method to remove a task from the completed tasks list
@app.route('/delete/<int:_id>',methods=['GET'])
def delete_task(_id):
    """ delete the specified task """
    try:
        #try delete request on the server to remove the specified task
        delete(SERVER_URL+f'delete/{_id}')
    except:
        #generate 404 error if an exception is thrown
        abort(404)
    #redirect to index page to view changes
    return redirect('/',308)

#API program start point ----->
if __name__ == '__main__':
    app.run(debug=True)
