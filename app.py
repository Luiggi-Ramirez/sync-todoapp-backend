import datetime
import utils
from flask import Flask, request

PATH_BASE_API = '/api/v1'

app = Flask(__name__)


@app.route('/')
def index():
    """Index route"""
    data = {
        "code": 200,
        "msg": "Online"
    }
    return data


@app.route(f'{PATH_BASE_API}/user/login', methods=['POST', 'GET'])
def login():
    """Funtion to recive a json with email and password and send it to the database
    Return
    ---------
    json: json
        A json with info about the correct login
    """
    if request.method == 'POST':
        data = request.json
        email = data['email']
        password = data['password']
        msg, is_ok = utils.db_select_user(email, password)
    elif request.method == 'GET':
        msg = 'Login'
    if is_ok:
        return {
            "code": 200,
            "msg": msg
        }
    else:
        return {
            "code": 401,
            "msg": msg
        }, 401


@app.route(f'{PATH_BASE_API}/user/create', methods=['POST', 'GET'])
def create_user():
    """Funtion to recive a json with name, last_name, email, password and confirmation password and send it to the database
    ---------
    Return
    ---------
    json: json
        A json with info about the send of user 
    """
    if request.method == 'POST':
        created = datetime.datetime.now()
        data = request.json
        name = data['name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']
        msg = utils.db_create_user(name, last_name, email, password, confirm_password, created)
    elif request.method == 'GET':
        msg = 'Registro de nuevo usuario'
    return {
        "code": 200,
        "msg": msg
    }


@app.route(f'{PATH_BASE_API}/task/create/<int:usuarios_user_id>', methods=['POST', 'GET'])
def create_task(usuarios_user_id):
    """Funtion to recive a json with title, description, end day, start day, time, id priority, if is completed and send it to the database
    Parameters
    ----------
    usuarios_user_id: int
        Id user founded in table user
    ---------
    Return
    ---------
    json: json
        A json with info about the send of the task
    """
    if request.method == 'POST':
        data = request.json
        title = data['title']
        description = data['description']
        end_date = data['end_date']
        start_date = data['start_date']
        time = data['time']
        id_priority = data['id_priority']
        is_completed = data['is_completed']
        msg = utils.db_create_task(title, description, end_date, start_date, time, id_priority, is_completed, usuarios_user_id)
    elif request.method == 'GET': 
        msg = 'Crea una nueva tarea'
    return {
        "code": 200,
        "msg": msg
    }


@app.route(f'{PATH_BASE_API}/task/show/<int:task_id>', methods=['GET'])
def show_task(task_id):
    """Funtion to recive a task from the database
    Parameters
    ----------
    id_task: int
        Id task founded in table task
    ---------
    Return
    ---------
    json: json
        A json with the task
    """
    lst = utils.db_get_task(task_id)
    if lst == []:
        return {
            "code": 404,
            "msg": 'Tarea no encontrada'
        }, 404
    else:
        for data in lst:
            task = {
                "task_id": task_id,
                "title": data[1],
                "description": data[2],
                "end_date" : str(data[3]),
                "start_date" : str(data[4]),
                "time": str(data[5]),
                "id_priority" : data[6],
                "is_completed": data[7]
            }
        return {
            "code": 200,
            "task": task
        }


@app.route(f'{PATH_BASE_API}/tasks/all/<int:users_user_id>', methods=['GET'])
def show_tasks(users_user_id):
    """Funtion to recive tasks from the database
    Parameters
    ----------
    usuarios_user_id: int
        Id user founded in table user
    ---------
    Return
    ---------
    json: json
        A json with the tasks
    """
    lst = utils.db_get_tasks(users_user_id)
    new_lst = []
    if lst == []:
        return {
            "code": 404,
            "msg" : 'Tarea no encontrada'
        }, 404
    else:
        for data in lst:
            task = {
                "id_user": users_user_id,
                "title": data[1],
                "description": data[2],
                "end_date" : str(data[3]),
                "start_date" : str(data[4]),
                "time": str(data[5]),
                "id_priority" : data[6],
                "is_completed": data[7]
            }
            new_lst.append(task)
        return {
            "code": 200,
            "tasks": new_lst
        }
    

@app.route(f'{PATH_BASE_API}/task/update/<int:task_id>', methods=['POST', 'GET'])
def update_task(task_id):
    """Funtion to recive a json with info to update a task and send it to the database
    Parameters
    ----------
    task_id: int
        Id task founded in table task
    ---------
    Return
    ---------
    json: json
        A json with info about the upgrade
    """
    if request.method == 'POST':
        data = request.json
        title = data['title']
        description = data['description']
        end_date = data['end_date']
        start_date = data['start_date']
        time = data['time']
        id_priority = data['id_priority']
        is_completed = data['is_completed']
        msg, is_ok = utils.db_update_task(task_id, title, description, end_date, start_date, time, id_priority, is_completed)
    elif request.method == 'GET':
        msg = 'Actualiza una tarea'
    if is_ok == True:
        return {
            "code": 200,
            "msg": msg
        }    
    else:
        return {
            "code": 404,
            "msg": msg
        }, 404    


@app.route(f'{PATH_BASE_API}/task/delete/<int:task_id>', methods=['DELETE', 'GET'])
def delete_task(task_id):
    """Funtion to delete a task from the database
    Parameters
    ----------
    task_id: int
        Id of task founded in table task
    ---------
    Return
    ---------
    json: json
        A json with info about the delete
    """
    if request.method == 'DELETE':
        msg, is_ok = utils.db_delete_task(task_id)
    elif request.method == 'GET':
        msg = 'Elimina una tarea'
    if is_ok == True:
        return {
            "code": 200,
            "msg": msg
        }
    else:
        return {
            "code": 404,
            "msg": msg
        }, 404


if __name__ == '__main__':
    app.run(debug=True)







