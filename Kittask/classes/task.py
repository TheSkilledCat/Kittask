class Task:
    def __init__(self, task_id: int, owned_by: str, title: str, description: str, date_created: str,
                 date_modified: str, deadline: str = None, tags: str = None, completed: bool = False) -> None:
        self.task_id = task_id
        self.owned_by = owned_by
        self.title = title
        self.desc = description
        self.date_created = date_created
        self.date_modified = date_modified
        self.deadline = deadline
        self.tags = tags
        self.completed = completed

    def __str__(self):
        return f'''
        {self.task_id},
        {self.owned_by},
        {self.title},
        {self.desc},
        {self.date_created},
        {self.date_modified},
        {self.deadline},
        {self.tags},
        {self.completed}
        '''
