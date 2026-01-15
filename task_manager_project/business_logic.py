import datetime
from constants import TASK_MAX_LENGTH, PRIORITIES, STATUSES, DATE_FORMAT
from data_access import FileHandler

class Task:
    def __init__(self, id=None, title="", description="", priority="Medium", due_date=None, status="Pending", created_date=None):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.status = status
        self.created_date = created_date or datetime.date.today().strftime(DATE_FORMAT)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'status': self.status,
            'created_date': self.created_date
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d['id'],
            title=d['title'],
            description=d['description'],
            priority=d.get('priority', 'Medium'),
            due_date=d.get('due_date'),
            status=d.get('status', 'Pending'),
            created_date=d.get('created_date')
        )

    def validate(self):
        if not self.title or len(self.title) > TASK_MAX_LENGTH:
            raise ValueError("Title is required and must be <= 100 characters")
        if len(self.description) > TASK_MAX_LENGTH:
            raise ValueError("Description must be <= 100 characters")
        if self.priority not in PRIORITIES:
            raise ValueError(f"Priority must be one of {PRIORITIES}")
        if self.status not in STATUSES:
            raise ValueError(f"Status must be one of {STATUSES}")
        if self.due_date:
            try:
                datetime.datetime.strptime(self.due_date, DATE_FORMAT)
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format")

    def __str__(self):
        return f"{self.id}: {self.title} - {self.description} (Priority: {self.priority}, Status: {self.status}, Due: {self.due_date})"

class TaskManager:
    def __init__(self, file_handler=None):
        self.file_handler = file_handler or FileHandler()

    def get_all_tasks(self):
        task_dicts = self.file_handler.load_tasks()
        return [Task.from_dict(td) for td in task_dicts]

    def get_task_by_id(self, task_id):
        tasks = self.get_all_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def add_task(self, title, description, priority="Medium", due_date=None):
        task_id = self.file_handler.get_next_id()
        task = Task(id=task_id, title=title, description=description, priority=priority, due_date=due_date)
        task.validate()
        self.file_handler.save_task(task.to_dict())
        return task

    def update_task(self, task_id, **kwargs):
        tasks = self.get_all_tasks()
        for task in tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                task.validate()
                self.file_handler.update_task(task_id, task.to_dict())
                return task
        raise ValueError("Task not found")

    def delete_task(self, task_id):
        self.file_handler.delete_task(task_id)

    def mark_complete(self, task_id):
        return self.update_task(task_id, status="Completed")

    def filter_tasks(self, status=None, priority=None):
        tasks = self.get_all_tasks()
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        return tasks

    def sort_tasks(self, by='created_date', reverse=False):
        tasks = self.get_all_tasks()
        if by == 'priority':
            priority_order = {p: i for i, p in enumerate(PRIORITIES)}
            tasks.sort(key=lambda t: priority_order.get(t.priority, 0), reverse=reverse)
        elif by == 'due_date':
            tasks.sort(key=lambda t: t.due_date or '9999-99-99', reverse=reverse)
        else:
            tasks.sort(key=lambda t: getattr(t, by, ''), reverse=reverse)
        return tasks