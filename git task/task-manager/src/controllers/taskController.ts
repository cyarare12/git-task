class TaskController {
    constructor(private taskService: any) {}

    async createTask(req: any, res: any) {
        try {
            const taskData = req.body;
            const newTask = await this.taskService.createTask(taskData);
            res.status(201).json(newTask);
        } catch (error) {
            res.status(400).json({ message: error.message });
        }
    }

    async viewTasks(req: any, res: any) {
        try {
            const tasks = await this.taskService.getAllTasks();
            res.status(200).json(tasks);
        } catch (error) {
            res.status(500).json({ message: error.message });
        }
    }

    async updateTask(req: any, res: any) {
        try {
            const taskId = req.params.id;
            const updatedData = req.body;
            const updatedTask = await this.taskService.updateTask(taskId, updatedData);
            res.status(200).json(updatedTask);
        } catch (error) {
            res.status(400).json({ message: error.message });
        }
    }

    async deleteTask(req: any, res: any) {
        try {
            const taskId = req.params.id;
            await this.taskService.deleteTask(taskId);
            res.status(204).send();
        } catch (error) {
            res.status(400).json({ message: error.message });
        }
    }
}

export default TaskController;