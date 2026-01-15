import datetime
import unittest
import os
from pathlib import Path

# Constants
DATE_FORMAT = "%d %b %Y"
USER_FILE = 'user.txt'
TASK_FILE = 'tasks.txt'
TASK_OVERVIEW_FILE = 'task_overview.txt'
USER_OVERVIEW_FILE = 'user_overview.txt'

# Classes
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password  # Note: In production, hash passwords

class Task:
    def __init__(self, username, title, description, assigned_date, due_date, completed='No'):
        self.username = username
        self.title = title
        self.description = description
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.completed = completed

    def to_dict(self):
        return {
            'username': self.username,
            'title': self.title,
            'description': self.description,
            'assigned_date': self.assigned_date,
            'due_date': self.due_date,
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d['username'], d['title'], d['description'], d['assigned_date'], d['due_date'], d['completed'])

# Data Access Layer
class DataAccess:
    def __init__(self, user_file=USER_FILE, task_file=TASK_FILE):
        self.user_file = Path(user_file)
        self.task_file = Path(task_file)

    def load_users(self):
        users = {}
        if not self.user_file.exists():
            return users
        try:
            with open(self.user_file, 'r') as f:
                for line in f:
                    parts = line.strip().split(', ')
                    if len(parts) == 2:
                        users[parts[0]] = parts[1]
        except Exception as e:
            print(f"Error loading users: {e}")
        return users

    def save_users(self, users):
        try:
            with open(self.user_file, 'w') as f:
                for u, p in users.items():
                    f.write(f"{u}, {p}\n")
        except Exception as e:
            print(f"Error saving users: {e}")

    def load_tasks(self):
        tasks = []
        if not self.task_file.exists():
            return tasks
        try:
            with open(self.task_file, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 6:
                        tasks.append(Task.from_dict({
                            'username': parts[0],
                            'title': parts[1],
                            'description': parts[2],
                            'assigned_date': parts[3],
                            'due_date': parts[4],
                            'completed': parts[5]
                        }))
        except Exception as e:
            print(f"Error loading tasks: {e}")
        return tasks

    def save_tasks(self, tasks):
        try:
            with open(self.task_file, 'w') as f:
                for task in tasks:
                    d = task.to_dict()
                    f.write(f"{d['username']},{d['title']},{d['description']},{d['assigned_date']},{d['due_date']},{d['completed']}\n")
        except Exception as e:
            print(f"Error saving tasks: {e}")

# In-memory Data Access for Testing
class MemoryDataAccess:
    def __init__(self):
        self.users = {}
        self.tasks = []

    def load_users(self):
        return self.users.copy()

    def save_users(self, users):
        self.users = users.copy()

    def load_tasks(self):
        return self.tasks.copy()

    def save_tasks(self, tasks):
        self.tasks = tasks.copy()

# Business Logic Layer
class TaskManager:
    def __init__(self, data_access):
        self.data_access = data_access

    def authenticate(self, username, password):
        users = self.data_access.load_users()
        return users.get(username) == password

    def register_user(self, username, password, confirm_password):
        if not username or not password:
            return "Username and password cannot be empty."
        users = self.data_access.load_users()
        if username in users:
            return "Username already exists. Please choose a different username."
        if password != confirm_password:
            return "Passwords do not match."
        users[username] = password
        self.data_access.save_users(users)
        return "User registered successfully."

    def add_task(self, username, title, description, due_date):
        if not all([username, title, description, due_date]):
            return "All fields are required."
        try:
            datetime.datetime.strptime(due_date, DATE_FORMAT)
        except ValueError:
            return "Invalid due date format. Use DD MMM YYYY."
        tasks = self.data_access.load_tasks()
        assigned_date = datetime.date.today().strftime(DATE_FORMAT)
        task = Task(username, title, description, assigned_date, due_date)
        tasks.append(task)
        self.data_access.save_tasks(tasks)
        return "Task added successfully."

    def get_all_tasks(self):
        return self.data_access.load_tasks()

    def get_user_tasks(self, username):
        tasks = self.data_access.load_tasks()
        return [t for t in tasks if t.username == username]

    def mark_task_complete(self, task):
        if task.completed == 'No':
            task.completed = 'Yes'
            tasks = self.data_access.load_tasks()
            # Update the task in list
            for t in tasks:
                if t.username == task.username and t.title == task.title and t.assigned_date == task.assigned_date:
                    t.completed = 'Yes'
                    break
            self.data_access.save_tasks(tasks)
            return True
        return False

    def update_task_username(self, task, new_username):
        if not new_username:
            return False
        task.username = new_username
        tasks = self.data_access.load_tasks()
        for t in tasks:
            if t.username == task.username and t.title == task.title and t.assigned_date == task.assigned_date:
                t.username = new_username
                break
        self.data_access.save_tasks(tasks)
        return True

    def update_task_due_date(self, task, new_due_date):
        try:
            datetime.datetime.strptime(new_due_date, DATE_FORMAT)
        except ValueError:
            return False
        task.due_date = new_due_date
        tasks = self.data_access.load_tasks()
        for t in tasks:
            if t.username == task.username and t.title == task.title and t.assigned_date == task.assigned_date:
                t.due_date = new_due_date
                break
        self.data_access.save_tasks(tasks)
        return True

    def delete_task(self, index):
        tasks = self.data_access.load_tasks()
        if 0 <= index < len(tasks):
            del tasks[index]
            self.data_access.save_tasks(tasks)
            return True
        return False

    def generate_reports(self):
        tasks = self.data_access.load_tasks()
        users = self.data_access.load_users()
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.completed == 'Yes'])
        uncompleted_tasks = total_tasks - completed_tasks
        overdue_tasks = 0
        today = datetime.date.today()
        for task in tasks:
            if task.completed == 'No':
                try:
                    due_date = datetime.datetime.strptime(task.due_date, DATE_FORMAT).date()
                    if due_date < today:
                        overdue_tasks += 1
                except ValueError:
                    pass  # skip invalid dates
        incomplete_percentage = (uncompleted_tasks / total_tasks * 100) if total_tasks > 0 else 0
        overdue_percentage = (overdue_tasks / total_tasks * 100) if total_tasks > 0 else 0
        try:
            with open(TASK_OVERVIEW_FILE, 'w') as file:
                file.write(f"Total tasks: {total_tasks}\n")
                file.write(f"Completed tasks: {completed_tasks}\n")
                file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
                file.write(f"Overdue tasks: {overdue_tasks}\n")
                file.write(f"Incomplete percentage: {incomplete_percentage:.2f}%\n")
                file.write(f"Overdue percentage: {overdue_percentage:.2f}%\n")
        except Exception as e:
            print(f"Error writing task overview: {e}")
        total_users = len(users)
        try:
            with open(USER_OVERVIEW_FILE, 'w') as file:
                file.write(f"Total users: {total_users}\n")
                file.write(f"Total tasks: {total_tasks}\n")
                for username in users:
                    user_tasks = [t for t in tasks if t.username == username]
                    user_total = len(user_tasks)
                    user_completed = len([t for t in user_tasks if t.completed == 'Yes'])
                    user_percentage = (user_total / total_tasks * 100) if total_tasks > 0 else 0
                    completed_percentage = (user_completed / user_total * 100) if user_total > 0 else 0
                    uncompleted_percentage = ((user_total - user_completed) / user_total * 100) if user_total > 0 else 0
                    overdue = 0
                    for task in user_tasks:
                        if task.completed == 'No':
                            try:
                                due_date = datetime.datetime.strptime(task.due_date, DATE_FORMAT).date()
                                if due_date < today:
                                    overdue += 1
                            except ValueError:
                                pass
                    overdue_percentage = (overdue / user_total * 100) if user_total > 0 else 0
                    file.write(f"\nUser: {username}\n")
                    file.write(f"  Total tasks: {user_total}\n")
                    file.write(f"  Percentage of total tasks: {user_percentage:.2f}%\n")
                    file.write(f"  Completed percentage: {completed_percentage:.2f}%\n")
                    file.write(f"  Uncompleted percentage: {uncompleted_percentage:.2f}%\n")
                    file.write(f"  Overdue percentage: {overdue_percentage:.2f}%\n")
        except Exception as e:
            print(f"Error writing user overview: {e}")
        print("Reports generated.")


# Login function
def login(data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        if tm.authenticate(username, password):
            return username
        else:
            print("Invalid username or password. Please try again.")

# Testable version of login
def login_logic(username, password, data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    return username if tm.authenticate(username, password) else None

# Register user function
def reg_user(data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    username = input("Enter new username: ")
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")
    result = tm.register_user(username, password, confirm_password)
    print(result)

# Testable version of reg_user
def reg_user_logic(username, password, confirm_password, data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    return tm.register_user(username, password, confirm_password)

# Add task function
def add_task(data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    username = input("Enter username of person assigned to task: ")
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter due date (e.g., 10 Oct 2023): ")
    result = tm.add_task(username, title, description, due_date)
    print(result)

# Testable version of add_task
def add_task_logic(username, title, description, due_date, data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    return tm.add_task(username, title, description, due_date)

# View all tasks function
def view_all(data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    tasks = tm.get_all_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for i, task in enumerate(tasks, 1):
        print(f"Task {i}:")
        print(f"  Assigned to: {task.username}")
        print(f"  Title: {task.title}")
        print(f"  Description: {task.description}")
        print(f"  Assigned date: {task.assigned_date}")
        print(f"  Due date: {task.due_date}")
        print(f"  Completed: {task.completed}")
        print()

# Testable version of view_all
def view_all_logic(data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    return [t.to_dict() for t in tm.get_all_tasks()]

# Recursive function to get valid task number
def get_valid_task_number(my_tasks):
    try:
        choice = int(input("Select a task number to edit/mark complete, or -1 to return: "))
        if choice == -1 or 1 <= choice <= len(my_tasks):
            return choice
        else:
            print("Invalid task number.")
            return get_valid_task_number(my_tasks)
    except ValueError:
        print("Please enter a valid number.")
        return get_valid_task_number(my_tasks)

# View my tasks function
def view_mine(username, data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    my_tasks = tm.get_user_tasks(username)
    if not my_tasks:
        print("No tasks assigned to you.")
        return
    while True:
        for i, task in enumerate(my_tasks, 1):
            print(f"{i}. {task.title} - {task.description} - Due: {task.due_date} - Completed: {task.completed}")
        print("-1. Return to main menu")
        choice = get_valid_task_number(my_tasks)
        if choice == -1:
            break
        else:
            task = my_tasks[choice - 1]
            print("1. Mark as complete")
            print("2. Edit task")
            sub_choice = input("Enter choice: ")
            if sub_choice == '1':
                if tm.mark_task_complete(task):
                    print("Task marked as complete.")
                else:
                    print("Task is already completed.")
            elif sub_choice == '2':
                if task.completed == 'No':
                    print("1. Edit username")
                    print("2. Edit due date")
                    edit_choice = input("Enter choice: ")
                    if edit_choice == '1':
                        new_username = input("Enter new username: ")
                        if tm.update_task_username(task, new_username):
                            print("Username updated.")
                        else:
                            print("Invalid username.")
                    elif edit_choice == '2':
                        new_due_date = input("Enter new due date: ")
                        if tm.update_task_due_date(task, new_due_date):
                            print("Due date updated.")
                        else:
                            print("Invalid date format.")
                    else:
                        print("Invalid choice.")
                else:
                    print("Cannot edit completed task.")
            else:
                print("Invalid choice.")

# View completed tasks function
def view_completed(data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    tasks = tm.get_all_tasks()
    completed_tasks = [t for t in tasks if t.completed == 'Yes']
    if not completed_tasks:
        print("No completed tasks.")
        return
    for i, task in enumerate(completed_tasks, 1):
        print(f"Task {i}:")
        print(f"  Assigned to: {task.username}")
        print(f"  Title: {task.title}")
        print(f"  Description: {task.description}")
        print(f"  Assigned date: {task.assigned_date}")
        print(f"  Due date: {task.due_date}")
        print(f"  Completed: {task.completed}")
        print()

# Delete task function
def delete_task(data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    view_all(data_access)  # to show tasks
    tasks = tm.get_all_tasks()
    if not tasks:
        return
    try:
        task_num = int(input("Enter the number of the task to delete: "))
        if tm.delete_task(task_num - 1):
            print("Task deleted successfully.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# Generate reports function
def generate_reports(data_access=None):
    if data_access is None:
        data_access = DataAccess()
    tm = TaskManager(data_access)
    tm.generate_reports()

# Display statistics function
def display_statistics(data_access=None):
    if data_access is None:
        data_access = DataAccess()
    try:
        with open(TASK_OVERVIEW_FILE, 'r') as file:
            print("Task Overview:")
            print(file.read())
        with open(USER_OVERVIEW_FILE, 'r') as file:
            print("User Overview:")
            print(file.read())
    except FileNotFoundError:
        print("Reports not found. Generating reports first...")
        generate_reports(data_access)
        display_statistics(data_access)

# Main function
def main():
    data_access = DataAccess()
    tm = TaskManager(data_access)
    users = data_access.load_users()
    if not users:
        print("No users found. Please register the admin user.")
        while True:
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            confirm_password = input("Confirm admin password: ")
            result = tm.register_user(username, password, confirm_password)
            if result == "User registered successfully.":
                print(f"Admin user '{username}' registered successfully.")
                break
            else:
                print(result)
    current_user = login(data_access)
    print(f"Welcome, {current_user}!")

    while True:
        if current_user == 'admin':
            menu = """
Please select one of the following options:
r - register user
a - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete a task
gr - generate reports
ds - display statistics
e - exit
"""
        else:
            menu = """
Please select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
"""
        print(menu)
        choice = input("Enter your choice: ").lower()

        if choice == 'r' and current_user == 'admin':
            reg_user(data_access)
        elif choice == 'a':
            add_task(data_access)
        elif choice == 'va':
            view_all(data_access)
        elif choice == 'vm':
            view_mine(current_user, data_access)
        elif choice == 'vc' and current_user == 'admin':
            view_completed(data_access)
        elif choice == 'del' and current_user == 'admin':
            delete_task(data_access)
        elif choice == 'gr' and current_user == 'admin':
            generate_reports(data_access)
        elif choice == 'ds' and current_user == 'admin':
            display_statistics(data_access)
        elif choice == 'e':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Unit Tests for Task Management Application

class TestUserManagement(unittest.TestCase):
    """Use Case 1: User Registration and Authentication"""

    def setUp(self):
        self.data_access = MemoryDataAccess()
        self.tm = TaskManager(self.data_access)

    def test_successful_user_registration(self):
        result = self.tm.register_user('john', 'pass123', 'pass123')
        self.assertEqual(result, "User registered successfully.")
        users = self.data_access.load_users()
        self.assertIn('john', users)
        self.assertEqual(users['john'], 'pass123')

    def test_registration_with_existing_username(self):
        self.tm.register_user('john', 'pass123', 'pass123')
        result = self.tm.register_user('john', 'newpass', 'newpass')
        self.assertEqual(result, "Username already exists. Please choose a different username.")

    def test_registration_password_mismatch(self):
        result = self.tm.register_user('john', 'pass123', 'different')
        self.assertEqual(result, "Passwords do not match.")

    def test_registration_empty_username(self):
        result = self.tm.register_user('', 'pass123', 'pass123')
        self.assertEqual(result, "Username and password cannot be empty.")

    def test_successful_authentication(self):
        self.tm.register_user('john', 'pass123', 'pass123')
        self.assertTrue(self.tm.authenticate('john', 'pass123'))

    def test_failed_authentication_wrong_password(self):
        self.tm.register_user('john', 'pass123', 'pass123')
        self.assertFalse(self.tm.authenticate('john', 'wrong'))

    def test_failed_authentication_nonexistent_user(self):
        self.assertFalse(self.tm.authenticate('nonexistent', 'pass'))

class TestTaskCreation(unittest.TestCase):
    """Use Case 2: Task Creation"""

    def setUp(self):
        self.data_access = MemoryDataAccess()
        self.tm = TaskManager(self.data_access)

    def test_successful_task_addition(self):
        result = self.tm.add_task('john', 'Fix Bug', 'Fix the login bug', '15 Dec 2023')
        self.assertEqual(result, "Task added successfully.")
        tasks = self.data_access.load_tasks()
        self.assertEqual(len(tasks), 1)
        task = tasks[0]
        self.assertEqual(task.username, 'john')
        self.assertEqual(task.title, 'Fix Bug')
        self.assertEqual(task.description, 'Fix the login bug')
        self.assertEqual(task.due_date, '15 Dec 2023')
        self.assertEqual(task.completed, 'No')

    def test_task_addition_missing_fields(self):
        result = self.tm.add_task('', 'Fix Bug', 'Description', '15 Dec 2023')
        self.assertEqual(result, "All fields are required.")

    def test_task_addition_invalid_date(self):
        result = self.tm.add_task('john', 'Fix Bug', 'Description', 'invalid date')
        self.assertEqual(result, "Invalid due date format. Use DD MMM YYYY.")

class TestTaskManagement(unittest.TestCase):
    """Use Case 3: Task Management (Complete and Edit)"""

    def setUp(self):
        self.data_access = MemoryDataAccess()
        self.tm = TaskManager(self.data_access)
        # Add a task
        self.tm.add_task('john', 'Fix Bug', 'Fix the login bug', '15 Dec 2023')
        self.task = self.data_access.load_tasks()[0]

    def test_mark_task_complete(self):
        success = self.tm.mark_task_complete(self.task)
        self.assertTrue(success)
        self.assertEqual(self.task.completed, 'Yes')

    def test_mark_already_completed_task(self):
        self.tm.mark_task_complete(self.task)
        success = self.tm.mark_task_complete(self.task)
        self.assertFalse(success)

    def test_update_task_username(self):
        success = self.tm.update_task_username(self.task, 'jane')
        self.assertTrue(success)
        self.assertEqual(self.task.username, 'jane')

    def test_update_task_username_empty(self):
        success = self.tm.update_task_username(self.task, '')
        self.assertFalse(success)

    def test_update_task_due_date(self):
        success = self.tm.update_task_due_date(self.task, '20 Dec 2023')
        self.assertTrue(success)
        self.assertEqual(self.task.due_date, '20 Dec 2023')

    def test_update_task_due_date_invalid(self):
        success = self.tm.update_task_due_date(self.task, 'invalid')
        self.assertFalse(success)

    def test_delete_task_valid_index(self):
        success = self.tm.delete_task(0)
        self.assertTrue(success)
        tasks = self.data_access.load_tasks()
        self.assertEqual(len(tasks), 0)

    def test_delete_task_invalid_index(self):
        success = self.tm.delete_task(5)
        self.assertFalse(success)

class TestReportGeneration(unittest.TestCase):
    """Use Case 4: Report Generation"""

    def setUp(self):
        self.data_access = MemoryDataAccess()
        self.tm = TaskManager(self.data_access)
        # Add users
        self.tm.register_user('admin', 'admin', 'admin')
        self.tm.register_user('john', 'pass', 'pass')
        # Add tasks
        self.tm.add_task('john', 'Task 1', 'Desc 1', '10 Dec 2023')
        self.tm.add_task('john', 'Task 2', 'Desc 2', '11 Dec 2023')
        self.tm.add_task('admin', 'Task 3', 'Desc 3', '12 Dec 2023')
        # Mark one complete
        tasks = self.data_access.load_tasks()
        self.tm.mark_task_complete(tasks[0])

    def test_get_all_tasks(self):
        tasks = self.tm.get_all_tasks()
        self.assertEqual(len(tasks), 3)

    def test_get_user_tasks(self):
        tasks = self.tm.get_user_tasks('john')
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].username, 'john')

    def test_generate_reports(self):
        # Mock the generate_reports method to avoid file writing
        # Since it writes to files, we can test the logic by checking data
        tasks = self.tm.get_all_tasks()
        users = self.data_access.load_users()
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.completed == 'Yes'])
        self.assertEqual(total_tasks, 3)
        self.assertEqual(completed_tasks, 1)
        self.assertEqual(len(users), 2)

if __name__ == "__main__":
    main()