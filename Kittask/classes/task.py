
class Task:
    def __init__(self, task_id: str, owned_by: str, title: str, description: str, date_created: str,
                 date_modified: str, deadline: str = None, tags: str = None, status: bool = False):
        self.task_id = task_id
        self.owned_by = owned_by
        self.title = title
        self.desc = description
        self.date_created = date_created
        self.date_modified = date_modified
        self.deadline = deadline
        self.tags = tags
        self.status = status
