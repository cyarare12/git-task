from business_logic import TaskManager
from constants import PRIORITIES, STATUSES

def start_application():
    """Start the Task Management Application."""
    task_manager = TaskManager()

    while True:
        print("\nTask Management Application")
        print("1. View All Tasks")
        print("2. Add Task")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Filter Tasks")
        print("7. Sort Tasks")
        print("8. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            tasks = task_manager.get_all_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                print("Tasks:")
                for task in tasks:
                    print(f"- {task}")

        elif choice == "2":
            try:
                title = input("Enter task title: ").strip()
                description = input("Enter task description: ").strip()
                print(f"Priorities: {', '.join(PRIORITIES)}")
                priority = input(f"Enter priority ({PRIORITIES[1]}): ").strip() or PRIORITIES[1]
                due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip() or None
                task = task_manager.add_task(title, description, priority, due_date)
                print(f"Task added successfully! ID: {task.id}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            try:
                task_id = int(input("Enter task ID to update: ").strip())
                task = task_manager.get_task_by_id(task_id)
                if not task:
                    print("Task not found.")
                    continue
                print(f"Current task: {task}")
                title = input(f"New title ({task.title}): ").strip() or task.title
                description = input(f"New description ({task.description}): ").strip() or task.description
                print(f"Priorities: {', '.join(PRIORITIES)}")
                priority = input(f"New priority ({task.priority}): ").strip() or task.priority
                due_date = input(f"New due date ({task.due_date}): ").strip() or task.due_date
                task_manager.update_task(task_id, title=title, description=description, priority=priority, due_date=due_date)
                print("Task updated successfully!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            try:
                task_id = int(input("Enter task ID to delete: ").strip())
                task_manager.delete_task(task_id)
                print("Task deleted successfully!")
            except ValueError:
                print("Invalid ID.")

        elif choice == "5":
            try:
                task_id = int(input("Enter task ID to mark complete: ").strip())
                task_manager.mark_complete(task_id)
                print("Task marked as completed!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "6":
            print(f"Statuses: {', '.join(STATUSES)}")
            status = input("Filter by status (optional): ").strip() or None
            print(f"Priorities: {', '.join(PRIORITIES)}")
            priority = input("Filter by priority (optional): ").strip() or None
            tasks = task_manager.filter_tasks(status=status, priority=priority)
            if not tasks:
                print("No tasks match the filter.")
            else:
                print("Filtered Tasks:")
                for task in tasks:
                    print(f"- {task}")

        elif choice == "7":
            print("Sort by: created_date, priority, due_date")
            sort_by = input("Sort by (created_date): ").strip() or 'created_date'
            reverse = input("Reverse order? (y/n): ").strip().lower() == 'y'
            tasks = task_manager.sort_tasks(by=sort_by, reverse=reverse)
            print("Sorted Tasks:")
            for task in tasks:
                print(f"- {task}")

        elif choice == "8":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")