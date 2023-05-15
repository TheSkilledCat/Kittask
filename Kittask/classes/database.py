#####################################################################################
# Inja yek classe Database be onvane library baraye karaye database sakhtam.
# Function haye asli az in class estefade mikonan ta data taghir bedan.
#####################################################################################

import sqlite3
import random
import hashlib

from .task import Task


class Database:
    db = sqlite3.connect("./database.sqlite")
    cur = db.cursor()

    def __init__(self):
        self.create_tables()

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users(
        user_id TEXT PRIMARY KEY,
        username TEXT,
        phone TEXT,
        password TEXT
    )
''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS tasks(
        task_id TEXT PRIMARY KEY,
        title TEXT,
        desc TEXT,
        date_created DATE,
        date_modified DATE,
        deadline DATE,
        tags TEXT,
        status BOOL
    )
''')
        self.db.commit()

    ##############################################
    #                TASK SYSTEM                 #

    def create_task_id(self):
        self.cur.execute('''SELECT task_id FROM tasks''')
        current_ids = self.cur.fetchall()
        created_id = f"{random.randint(0, 99999):05d}"
        if created_id in current_ids:
            self.create_task_id()
        return created_id

    def add_task(self, task: Task):
        self.cur.execute('''INSERT INTO polls(poll_id, owned_by, title, is_active)
                          VALUES(?,?,?,?)''', (task.poll_id, task.owned_by, task.title, task.is_active))

        option_index = 0
        for option in task.options:
            option_id = int(str(task.poll_id) + '00' + str(option_index))
            option_index += 1
            self.cur.execute('''INSERT INTO options(option_id, poll_id, option_index, option_title, votes)
                              VALUES(?,?,?,?,?)''', (option_id, task.poll_id, option_index, option, 0))
        self.db.commit()

    @classmethod
    def change_status(cls, poll_id):
        if not cls.poll_exists(poll_id):
            return print("\033[0;31m[ERROR] Wrong poll id. Please try again.\033[0m")
        status = cls.cur.execute('''SELECT is_active FROM polls WHERE poll_id = ?''', (poll_id,)).fetchone()[0]
        if status:
            status = False
        else:
            status = True
        cls.cur.execute('''UPDATE polls SET is_active = ? WHERE poll_id = ?''', (status, poll_id))
        cls.db.commit()
        return

    @classmethod
    def poll_exists(cls, poll_id):
        poll_id = cls.cur.execute('''SELECT * FROM polls WHERE poll_id=?''',
                                  (poll_id,)).fetchone()
        return True if poll_id is not None else False

    @classmethod
    def get_all_polls(cls):
        return cls.cur.execute('''SELECT poll_id, title FROM polls''').fetchall()

    @classmethod
    def get_active_polls(cls):
        return cls.cur.execute('''SELECT poll_id, title FROM polls WHERE is_active = 1''').fetchall()

    @classmethod
    def get_owned_polls(cls, user):
        polls = cls.cur.execute('''SELECT poll_id FROM polls WHERE owned_by = ?''', (user,)).fetchall()
        final_polls = []
        for i in polls:
            final_polls.append(cls.get_poll(i[0]))
        return final_polls

    @classmethod
    def get_poll(self, poll_id: int):
        poll = self.cur.execute('''SELECT * FROM polls WHERE poll_id = ?''', (poll_id,)).fetchone()
        if poll is None:
            print("\033[0;31m[ERROR] Wrong poll id. Please try again.\033[0m")
            return None
        self.cur.execute(f'''SELECT option_title FROM options WHERE poll_id = ? ORDER BY option_index''', (poll_id,))
        options = []
        for option in self.cur.fetchall():
            options.append(option[0])
        return Poll(poll[0], poll[1], poll[2], options, poll[3])

    @classmethod
    def add_vote(self, poll_id, user, vote):
        self.cur.execute(f'''UPDATE options SET votes = votes + 1 WHERE poll_id = ? AND option_index = ?''',
                         (poll_id, vote,))
        self.cur.execute(f'''INSERT INTO votes(poll_id, user, vote) VALUES(?, ?, ?)''', (poll_id, user, vote))
        self.db.commit()

    @classmethod
    def has_voted(cls, poll_id, user):
        cls.cur.execute('''SELECT * FROM votes WHERE poll_id = ? AND user = ?''', (poll_id, user,))
        return True if len(cls.cur.fetchall()) > 0 else False

    @classmethod
    def get_results(cls, poll_id):
        results = cls.cur.execute('''SELECT votes FROM options WHERE poll_id = ?''', (poll_id,)).fetchall()
        final_results = []
        for i in results:
            final_results.append(i[0])
        return final_results

    ##############################################
    #                USER SYSTEM                 #

    @classmethod
    def user_exists(cls, user):
        user = cls.cur.execute('''SELECT * FROM users WHERE username = ? OR phone = ?''',
                               (user, user)).fetchone()
        return True if user is not None else False

    @classmethod
    def add_user(cls, username, password, phone):
        secured_pass = hashlib.sha256((password + "TaskManager").encode())
        final_pass = secured_pass.hexdigest()
        if not cls.user_exists(username) and not cls.user_exists(phone):
            cls.cur.execute('''INSERT INTO users(username, password, phone) VALUES(?,?,?)''',
                            (username, final_pass, phone))
            cls.db.commit()
            return
        else:
            return print(f"\033[0;31m[ERROR] Account already exists. Please try again.\033[0m")

    @classmethod
    def get_password(cls, user):
        if cls.user_exists(user):
            cls.cur.execute('''SELECT password FROM users WHERE username = ?''', (user,))
            return cls.cur.fetchone()[0]

    @classmethod
    def password_matches(cls, user, password):
        if cls.user_exists(user):
            fetched_pass = cls.cur.execute('''SELECT password FROM users WHERE username = ?''', (user,)).fetchone()[0]
            secured_pass = hashlib.sha256((password + "TaskManager").encode())
            final_pass = secured_pass.hexdigest()
            return True if final_pass == fetched_pass else False
