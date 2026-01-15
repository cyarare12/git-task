class Task {
    private id: string;
    private title: string;
    private description: string;
    private priority: number;
    private dueDate: Date;
    private status: 'pending' | 'completed';
    private createdDate: Date;

    constructor(id: string, title: string, description: string, priority: number, dueDate: Date) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.priority = priority;
        this.dueDate = dueDate;
        this.status = 'pending';
        this.createdDate = new Date();
    }

    public markComplete(): void {
        this.status = 'completed';
    }

    public updateTask(title?: string, description?: string, priority?: number, dueDate?: Date): void {
        if (title) this.title = title;
        if (description) this.description = description;
        if (priority) this.priority = priority;
        if (dueDate) this.dueDate = dueDate;
    }

    public validate(): boolean {
        if (!this.title || !this.description || this.priority < 1 || !this.dueDate) {
            return false;
        }
        return true;
    }

    // Getters
    public getId(): string {
        return this.id;
    }

    public getTitle(): string {
        return this.title;
    }

    public getDescription(): string {
        return this.description;
    }

    public getPriority(): number {
        return this.priority;
    }

    public getDueDate(): Date {
        return this.dueDate;
    }

    public getStatus(): 'pending' | 'completed' {
        return this.status;
    }

    public getCreatedDate(): Date {
        return this.createdDate;
    }
}