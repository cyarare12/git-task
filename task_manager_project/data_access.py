import json
import os
from config import FILENAME

class FileHandler:
    def __init__(self, filename=None):
        self.filename = filename or FILENAME

    def load_tasks(self):
        """Load tasks from JSON file."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_task(self, task_dict):
        """Save a single task to the file."""
        tasks = self.load_tasks()
        tasks.append(task_dict)
        with open(self.filename, 'w') as f:
            json.dump(tasks, f, indent=4)

    def update_task(self, task_id, task_dict):
        """Update a task in the file."""
        tasks = self.load_tasks()
        for i, t in enumerate(tasks):
            if t['id'] == task_id:
                tasks[i] = task_dict
                break
        with open(self.filename, 'w') as f:
            json.dump(tasks, f, indent=4)

    def delete_task(self, task_id):
        """Delete a task from the file."""
        tasks = self.load_tasks()
        tasks = [t for t in tasks if t['id'] != task_id]
        with open(self.filename, 'w') as f:
            json.dump(tasks, f, indent=4)

    def get_next_id(self):
        """Get the next available ID."""
        tasks = self.load_tasks()
        if not tasks:
            return 1
        return max(t['id'] for t in tasks) + 1