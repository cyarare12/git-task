import { TaskController } from '../src/controllers/taskController';
import { Task } from '../src/models/task';
import { FileHandler } from '../src/services/fileHandler';

describe('TaskManager', () => {
    let taskController: TaskController;
    let fileHandler: FileHandler;

    beforeEach(() => {
        fileHandler = new FileHandler();
        taskController = new TaskController(fileHandler);
    });

    test('should create a new task', () => {
        const taskData = {
            title: 'Test Task',
            description: 'This is a test task',
            priority: 'High',
            dueDate: '2023-12-31'
        };

        const createdTask = taskController.createTask(taskData);
        expect(createdTask).toBeInstanceOf(Task);
        expect(createdTask.title).toBe(taskData.title);
    });

    test('should view all tasks', () => {
        taskController.createTask({
            title: 'Test Task 1',
            description: 'This is test task 1',
            priority: 'Medium',
            dueDate: '2023-12-31'
        });

        taskController.createTask({
            title: 'Test Task 2',
            description: 'This is test task 2',
            priority: 'Low',
            dueDate: '2023-12-31'
        });

        const tasks = taskController.viewTasks();
        expect(tasks.length).toBe(2);
    });

    test('should update a task', () => {
        const task = taskController.createTask({
            title: 'Task to Update',
            description: 'This task will be updated',
            priority: 'Low',
            dueDate: '2023-12-31'
        });

        const updatedData = {
            title: 'Updated Task',
            description: 'This task has been updated',
            priority: 'High',
            dueDate: '2024-01-01'
        };

        const updatedTask = taskController.updateTask(task.id, updatedData);
        expect(updatedTask.title).toBe(updatedData.title);
        expect(updatedTask.priority).toBe(updatedData.priority);
    });

    test('should delete a task', () => {
        const task = taskController.createTask({
            title: 'Task to Delete',
            description: 'This task will be deleted',
            priority: 'Low',
            dueDate: '2023-12-31'
        });

        taskController.deleteTask(task.id);
        const tasks = taskController.viewTasks();
        expect(tasks).not.toContainEqual(task);
    });
});