import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

try:
    conn = mysql.connector.connect(
        host = '192.168.100.50',
        port = 3306,
        user = 'admin',
        password = 'admin',
        db = 'todo_app'
    )
    cur = conn.cursor()
    print('Conexión establecida')
except Exception as err:
    print(err)


#Crea el usuario en la database
def db_create_user(name, last_name, email, password, confirm_password, created):
    """Function to create a new user and save it into the database
    Parameters
    --------------------------------
    name: str
        Name of new user
    last_name: str
        Lastname of new user
    email: str
        Email of new user
    password: str
        Password of new user
    confirm_user: str
        The same password of new user
    created: date
        Date of new user creation
    --------------------------------
    Return
    --------------------------------
    msg: str
        A confirmation message    
    """
    pass_cifr = generate_password_hash(password)
    same = check_password_hash(pass_cifr, confirm_password)
    if same:
        query = ("INSERT INTO `users` VALUES (%s, %s, %s, %s, %s, %s, %s)")
        parameters = (None, name, last_name, email, pass_cifr, pass_cifr, created)
        cur.execute(query, parameters)
        conn.commit()
        msg = 'Nuevo usuario creado'
    else:
        msg = 'Las contraseñas no coinciden'
    return msg


def db_create_task(title, description, end_date, start_date, time, id_priority, is_completed, user_user_id):
    """Function to create a new task and savi it into the databse
    Parameters
    --------------------------------
    title: str
        Title of the task
    description: str
        Description of the task
    end_date: str
        Task completion date
    start_date: str
        Task start date
    time: str
        Task completion time
    id_priority: int
        Id of priority
    is_completed: bool, optional
        Flag use to verify if the task is completed or not (default is False)
    user_user_id: int
        Id of user founded in user table
    --------------------------------
    Return
    --------------------------------
    msg: str
        A confirmation message    
    """
    try:
        query = ("INSERT INTO `task` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        parameters = (None, title, description, end_date, start_date, time, is_completed, id_priority, user_user_id)
        cur.execute(query, parameters)
        conn.commit()
        msg = 'Nueva tarea creada'
    except Exception as err:
        msg = 'Error al crear tarea'
    return msg


def db_select_user(email, password):
    """Function to check if the user is registered in the database
    Parameters
    --------------------------------
    email: str
        Email of user
    password: str
        Password of user
    --------------------------------
    Return
    --------------------------------
    msg: str
        A confirmation message    
    """
    try:
        email = email.replace(" ", "")
        query = "SELECT * FROM `users` WHERE `email` = %s"
        parameter = (email,)
        cur.execute(query, parameter)
        row = cur.fetchall()
        if email == row[0][3] and check_password_hash(row[0][4], password):
            msg = f'Bienvenido/a {row[0][1]} {row[0][2]}'
            is_ok = True
        else:
            msg = 'Correo o contraseña incorrectos'
            is_ok = False
    except:
        msg = 'Usuario no registrado'
        is_ok = False
    return msg, is_ok
    

def db_update_task(task_id, title, description, end_date, start_date, time, id_priority, is_completed, user_user_id):
    """Function to update task by task index in the database
    Parameters
    --------------------------------
    id_user: str
        Id of user founded in task table
    title: str
        New title of the task
    description: str
        New description of the task
    end_date: str
        New task completion date
    start_date: str
        New task start date
    time: str
        New task completion time
    id_priority: int
        New id of priority
    is_completed: bool
        Actualization of if the task is completed or not 
    user_user_id: int
        Id of user founded in user table
    --------------------------------
    Return
    --------------------------------
    msg: str
        A confirmation message    
    """
    try:
        query = "UPDATE `task` SET `title` = %s, `description` = %s, `end_date` = %s, `start_date` = %s, `created_time` = %s, `is_complete` = %s, `priority_priority_id` = %s WHERE `task_id` = %s AND `user_user_id`= %s"
        parameters = (title, description, end_date, start_date, time, is_completed, id_priority, task_id, user_user_id)
        cur.execute(query, parameters)
        conn.commit()
        msg = 'Tarea actualizada'
    except:
        msg = 'Actualización errónea'
    return msg


def db_get_tasks(user_user_id):
    """Function to obtain all tasks of the user from the database
    Parameters
    --------------------------------
    user_user_id: int
        Id of user founded in user table
    --------------------------------
    Return
    --------------------------------
    data: list
        A list with tuples of tasks
    """
    try:
        query = "SELECT * FROM `task` WHERE `user_user_id` = %s"
        parameters = (user_user_id,)
        cur.execute(query, parameters)
        data = cur.fetchall()
        return data
    except Exception as err:
        print(err)
        

def db_delete_task(user_user_id, task_id):
    """Function to delete a task from the database
    Parameters
    --------------------------------
    user_user_id: int
        Id of user founded in user table
    task_id: int
        Id of user founded in task table
    --------------------------------
    Return
    --------------------------------
    msg: str
        A confirmation message    
    """
    try:
        query = "DELETE FROM `task` WHERE `user_user_id` = %s AND `task_id` = %s"
        parameters = (user_user_id, task_id)
        cur.execute(query, parameters)
        conn.commit()
        msg = 'Tarea eliminada'
    except:
        msg = 'Error al eliminar'
    return msg






