import sqlite3
import random
import hashlib
from datetime import datetime

from Kittask.classes.task import Task


class Database:
    def __init__(self):
        pass

    def __enter__(self):
        self.db = sqlite3.connect("../../database.sqlite3")
        self.cur = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
        else:
            self.db.commit()
        self.db.close()

    @classmethod
    def create_tables(cls):
        with cls() as db:
            # db.cur.execute('''CREATE TABLE IF NOT EXISTS users (
            #     id INTEGER PRIMARY KEY NOT NULL,
            #     phone TEXT NOT NULL,
            #     password TEXT NOT NULL
            # )''')
            # db.cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
            #     id INTEGER PRIMARY KEY NOT NULL,
            #     title TEXT NOT NULL,
            #     description TEXT NOT NULL,
            #     date_created DATE NOT NULL,
            #     date_modified DATE NOT NULL,
            #     deadline DATE NOT NULL,
            #     tags TEXT NOT NULL,
            #     status BOOL NOT NULL
            # )''')
            db.cur.execute('''
                DROP TABLE IF EXISTS users;
            ''')
            db.cur.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT NOT NULL,
                    password TEXT NOT NULL
                );
            ''')
            db.cur.execute('''
                CREATE UNIQUE INDEX idx_users_phone ON users (phone);
            ''')

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        with cls() as db:
            db.create_tables()

    ##############################################
    #                TASK SYSTEM                 #

    @classmethod
    def create_task_id(cls):
        with cls() as db:
            db.cur.execute('''SELECT task_id FROM tasks''')
            current_ids = db.cur.fetchall()
            created_id = f"{random.randint(0, 99999):05d}"
            if created_id in current_ids:
                cls.create_task_id()
            return created_id

    @classmethod
    def add_task(cls, task: Task) -> None:
        with cls() as db:
            if cls.task_exists:
                return print(f"\033[0;31m[ERROR] Task already exists. Please try again.\033[0m")

            db.cur.execute('''INSERT INTO tasks(task_id, owned_by, title, description, date_created, date_modified, 
                                                 deadline, tags, status)
                              VALUES(?,?,?,?)''',
                           (task.task_id, task.owned_by, task.title, task.desc, task.date_created,
                            task.date_modified, task.deadline, task.tags, task.status))
            return

    @classmethod
    def change_status(cls, task_id):
        with cls() as db:
            if not cls.task_exists(task_id):
                return print("\033[0;31m[ERROR] Wrong task id. Please try again.\033[0m")
            status = db.cur.execute('''SELECT status FROM tasks WHERE task_id = ?''', (task_id,)).fetchone()[0]
            if status:
                status = False
            else:
                status = True
            db.cur.execute('''UPDATE tasks SET status = ? WHERE task_id = ?''', (status, task_id))
            return

    @classmethod
    def task_exists(cls, task_id) -> bool:
        with cls() as db:
            task_id = db.cur.execute('''SELECT * FROM tasks WHERE task_id = ?''',
                                     (task_id,)).fetchone()
            return True if task_id is not None else False

    @classmethod
    def get_task(cls, task_id: int):
        with cls() as db:
            task = db.cur.execute('''SELECT * FROM tasks WHERE task_id = ?''', (task_id,)).fetchone()
            if task is None:
                print("\033[0;31m[ERROR] Wrong task id. Please try again.\033[0m")
                return None
            return Task(task[0], task[1], task[2], task[3], task[5], task[6], task[7], task[8])

    @classmethod
    def get_owned_tasks_basic(cls, user_id: str):
        with cls() as db:
            return db.cur.execute('''SELECT task_id, title, date_created, date_modified, deadline FROM tasks 
                                      WHERE owned_by = ?''', (user_id,)).fetchall()

    @classmethod
    def get_owned_tasks(cls, user_id: str):
        with cls() as db:
            tasks_raw = db.cur.execute('''SELECT task_id FROM tasks WHERE user_id = ?''', (user_id,)).fetchall()
            tasks_cleaned = []
            for task_id in tasks_raw:
                tasks_cleaned.append(cls.get_task(task_id))
            return tasks_cleaned

    ##############################################
    #                USER SYSTEM                 #

    @classmethod
    def user_exists(cls, phone):
        with cls() as db:
            user = db.cur.execute('''SELECT * FROM users WHERE phone = ?''', (phone,)).fetchone()
            return True if user is not None else False

    @classmethod
    def add_user(cls, phone, password):
        with cls() as db:
            secured_pass = hashlib.sha256((password + "Kittask").encode())
            final_pass = secured_pass.hexdigest()
            if not cls.user_exists(phone):
                db.cur.execute('''INSERT INTO users(phone, password) VALUES(?,?)''',
                               (phone, final_pass))
                return
            else:
                return print(f"[ERROR] Account already exists. Please try again.")

    @classmethod
    def get_password(cls, user):
        with cls() as db:
            if cls.user_exists(user):
                db.cur.execute('''SELECT password FROM users WHERE phone = ?''', (user,))
                return db.cur.fetchone()[0]

    @classmethod
    def password_matches(cls, phone, password):
        with cls() as db:
            if cls.user_exists(phone):
                fetched_pass = db.cur.execute('''SELECT password FROM users WHERE phone = ?''', (phone,)).fetchone()[0]
                secured_pass = hashlib.sha256((password + "Kittask").encode())
                final_pass = secured_pass.hexdigest()
                return True if final_pass == fetched_pass else False

Database.create_tables()
