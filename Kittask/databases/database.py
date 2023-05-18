#################################################
#                Database Library               #
# Not using django's built-in database modeling #
#################################################


import sqlite3
import random
import hashlib

from Kittask.classes.date_time_module import DateTime as dt
from Kittask.classes.task import Task
from Kittask.classes.user import User
from Kittask.classes.verification import Verification


class Database:
    conn = sqlite3.connect("main.sqlite3", check_same_thread=False)
    cur = conn.cursor()

    def __init__(self):
        self.create_tables()

    @classmethod
    def create_tables(cls):
        cls.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                fullname TEXT NOT NULL,
                phone TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT
            )''')
        cls.cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY,
                owned_by TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                date_created DATETIME NOT NULL,
                date_modified DATETIME NOT NULL,
                deadline DATETIME,
                tags TEXT,
                completed BOOL NOT NULL
            )''')

    ##############################################
    #                TASK SYSTEM                 #
    ##############################################

    @classmethod
    def create_task_id(cls):
        cls.cur.execute('''SELECT task_id FROM tasks''')
        current_ids = cls.cur.fetchall()
        created_id = f"{random.randint(0, 99999):05d}"
        if created_id in current_ids:
            cls.create_task_id()
        return created_id

    @classmethod
    def add_task(cls, task: Task) -> None:
        if cls.task_exists(task.task_id):
            return

        cls.cur.execute('''INSERT INTO tasks(task_id, owned_by, title, description, date_created, date_modified, 
                                             deadline, tags, completed)
                          VALUES(?,?,?,?,?,?,?,?,?)''',
                        (task.task_id, task.owned_by, task.title, task.desc, task.date_created,
                         task.date_modified, task.deadline, task.tags, task.completed))
        cls.conn.commit()
        return

    @classmethod
    def modify_task(cls, task: Task) -> None:
        if not cls.task_exists(task.task_id):
            return

        cls.cur.execute('''UPDATE tasks
                           SET title = ?, description = ?, date_modified = ?, 
                               deadline = ?, tags = ?, completed = ?
                           WHERE task_id = ?''',
                        (task.title, task.desc, task.date_modified, task.deadline,
                         task.tags, task.completed, task.task_id))
        cls.conn.commit()
        return

    @classmethod
    def task_exists(cls, task_id: int) -> bool:
        task_id = cls.cur.execute('''SELECT * FROM tasks WHERE task_id = ?''',
                                  (task_id,)).fetchone()
        return True if task_id is not None else False

    @classmethod
    def change_status(cls, task_id):
        if not cls.task_exists(task_id):
            return
        status = cls.cur.execute('''SELECT completed FROM tasks WHERE task_id = ?''', (task_id,)).fetchone()[0]
        if status:
            status = False
        else:
            status = True
        cls.cur.execute('''UPDATE tasks SET completed = ? WHERE task_id = ?''', (status, task_id))
        cls.conn.commit()
        return

    @classmethod
    def get_task(cls, task_id: int):
        task = cls.cur.execute('''SELECT * FROM tasks WHERE task_id = ?''', (task_id,)).fetchone()
        if task is None:
            return None
        if task[8]:
            done_status = True
        else:
            done_status = False
        return Task(task[0], task[1], task[2], task[3], task[4], task[5], task[6], task[7], done_status)

    @classmethod
    def get_owned_tasks_basic(cls, user_id: str):
        return cls.cur.execute('''SELECT task_id, title, date_created, date_modified, deadline FROM tasks 
                                  WHERE owned_by = ?''', (user_id,)).fetchall()

    @classmethod
    def get_owned_tasks(cls, user_id: str):
        task_ids = cls.cur.execute('''SELECT task_id FROM tasks WHERE owned_by = ?''', (user_id,)).fetchall()
        tasks = []
        for task_id in task_ids:
            tasks.append(cls.get_task(task_id[0]))
        return tasks

    @classmethod
    def get_tasks_today(cls, user_id: str) -> list[Task]:
        tasks = cls.get_owned_tasks(user_id)
        tasks_today = []
        for task in tasks:
            if task.deadline is not None:
                if dt.get_date_from_fulldate(task.deadline) == dt.get_date_today():
                    tasks_today.append(task)
        return tasks_today

    @classmethod
    def get_owned_tags(cls, user_id: str):
        tasks = cls.get_owned_tasks(user_id)
        tags = []
        for task in tasks:
            for tag in task.tags.split(", "):
                if tag not in tags:
                    tags.append(tag)
        return tags

    @classmethod
    def get_all_tags(cls) -> list:
        tags = cls.cur.execute('''SELECT tags FROM tasks''').fetchall()
        all_tags = []
        for i in tags:
            i_tags = Verification.validate_tags_arr(i[0])
            for j in i_tags:
                if j not in all_tags:
                    all_tags += i_tags
        return all_tags

    @classmethod
    def set_as_done(cls, task_id):
        cls.cur.execute('''UPDATE tasks SET completed = 1 WHERE task_id = ?''', (task_id, ))
        cls.conn.commit()

    ##############################################
    #                USER SYSTEM                 #
    ##############################################

    @classmethod
    def user_exists(cls, phone):
        user = cls.cur.execute('''SELECT phone FROM users WHERE phone = ?''', (phone,)).fetchone()
        return True if user is not None else False

    @classmethod
    def add_user(cls, fullname, phone, password):
        secured_pass = hashlib.sha256((password + "Kittask").encode())
        final_pass = secured_pass.hexdigest()
        if not cls.user_exists(phone):
            cls.cur.execute('''INSERT INTO users(fullname, phone, password) VALUES(?,?,?)''',
                            (fullname, phone, final_pass))
            print("[DATABASE] User was added successfully.")
            cls.conn.commit()
            return None
        else:
            return print(f"[ERROR] Account already exists. Please try again.")

    @classmethod
    def get_user(cls, phone):
        user = cls.cur.execute('''SELECT * FROM users WHERE phone = ?''', (phone, )).fetchone()
        return User(user[1], user[2], user[3], user[4])

    @classmethod
    def get_password(cls, user):
        if cls.user_exists(user):
            cls.cur.execute('''SELECT password FROM users WHERE phone = ?''', (user,))
            return cls.cur.fetchone()[0]

    @classmethod
    def password_matches(cls, phone, password):
        if cls.user_exists(phone):
            fetched_pass = cls.cur.execute('''SELECT password FROM users WHERE phone = ?''', (phone,)).fetchone()[0]
            secured_pass = hashlib.sha256((password + "Kittask").encode())
            final_pass = secured_pass.hexdigest()
            return True if final_pass == fetched_pass else False
