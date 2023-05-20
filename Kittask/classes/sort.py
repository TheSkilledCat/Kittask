######################################
#        Task Sorting System         #
######################################

from datetime import datetime
from typing import Union

from .task import Task


class SortTasks:
    def __init__(self, tasks: list[Task], prompt: str, tags: Union[str, list] = ""):
        self.prompt = prompt
        self.tasks = tasks
        self.tags = tags

    ################################
    #    Sort Using Sort Prompt    #

    def sort_set(self) -> list:
        p = self.prompt
        if p[0] == "u":
            self.sort_by_dm()
        elif p[0] == "c":
            self.sort_by_dc()
        elif p[0] == "e":
            self.sort_by_dl()
        else:
            return []

        if p[1] == "d":
            self.sort_reverse()
        elif p[1] == "a":
            pass
        else:
            return []

        if p[2] == "g":
            self.sort_grouped()
        elif p[2] == "n":
            pass
        else:
            return []

        if self.tags:
            self.sort_set_filter()

        return self.tasks

    ################################
    #          Sort Modes          #

    def sort_by_dc(self):
        self.tasks.sort(key=lambda task: datetime.strptime(task.date_created, '%Y/%m/%d %H:%M'))

    def sort_by_dm(self):
        self.tasks.sort(key=lambda task: datetime.strptime(task.date_modified, '%Y/%m/%d %H:%M'))

    def sort_by_dl(self):
        no_deadline_tasks = []
        for task in self.tasks:
            if task.deadline is None:
                no_deadline_tasks.append(task)
                self.tasks.remove(task)

        self.tasks.sort(key=lambda task_with_deadline: datetime.strptime(task_with_deadline.deadline, '%Y/%m/%d %H:%M'))
        print([task.deadline for task in self.tasks])
        self.tasks += no_deadline_tasks

    def sort_reverse(self):
        self.tasks.reverse()

    def sort_grouped(self):
        new_array = []
        for task in self.tasks:
            if task.completed:
                new_array.append(task)
                self.tasks.remove(task)
        self.tasks += new_array

    def sort_set_filter(self):
        new_array = []
        for tag in self.tags:
            for task in self.tasks:
                task_tags = task.tags
                if tag in task_tags:
                    new_array.append(task)
        self.tasks = new_array
