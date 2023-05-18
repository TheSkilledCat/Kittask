import datetime

from Kittask.databases.database import Database
from .date_time_module import DateTime
from .task import Task


class Session:
    def __init__(self, phone: str, password: str):
        self.u = phone
        self.p = password
        self.db = Database()
        self.user = self.db.get_user(phone)
        self.db.get_all_tags()

    def create_task(self, task: Task):
        task.date_created = DateTime.get_datetime_now()
        task.date_modified = task.date_created
        self.db.add_task(task)

    def edit_task(self, task: Task):
        task.date_modified = DateTime.get_datetime_now()
        self.db.modify_task(task)

class Admin_Session(Session):
    pass
