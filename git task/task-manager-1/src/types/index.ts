export interface Task {
    id: string;
    title: string;
    description: string;
    priority: number;
    dueDate: Date;
    status: 'pending' | 'completed';
}

export interface User {
    id: string;
    username: string;
    email: string;
    password: string;
}